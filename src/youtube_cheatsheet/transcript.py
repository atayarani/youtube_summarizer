from sys import stderr

import youtube_transcript_api
from langchain.text_splitter import CharacterTextSplitter
from pytube import YouTube
from returns.converters import maybe_to_result
from returns.maybe import Maybe
from returns.pipeline import flow
from returns.result import Failure, Result, Success
from toolz import functoolz

import youtube_cheatsheet
import youtube_cheatsheet.ai_providers.assemblyai
import youtube_cheatsheet.exceptions
import youtube_cheatsheet.video_providers.youtube.audio


def get_transcript(video_id: str) -> Result[str, None]:
    safe_function = functoolz.excepts(
        (
            youtube_transcript_api._errors.NoTranscriptFound,
            youtube_transcript_api._errors.TranscriptsDisabled,
            youtube_transcript_api._errors.NoTranscriptAvailable,
        ),
        lambda id: youtube_transcript_api.YouTubeTranscriptApi.get_transcript(id),
        lambda _: None,
    )

    return maybe_to_result(
        Maybe.from_optional(safe_function(video_id)).bind_optional(
            lambda transcript: " ".join(format_transcript(transcript))
        )
    )


def format_transcript(transcript: dict) -> list[str]:
    return [item["text"] for item in transcript]


def set_transcript_pipe(youtube_video: YouTube) -> str:
    return flow(
        youtube_cheatsheet.transcript.get_transcript(youtube_video.video_id),
        lambda result: youtube_cheatsheet.transcript.handle_result(
            result, youtube_video
        ),
    )


def split(transcript: str) -> list[str] | youtube_cheatsheet.exceptions.TranscriptSplitError:
    chunks = flow(
        CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=10000,
            chunk_overlap=0,
        ),
        lambda transcript_splitter: transcript_splitter.split_text(transcript),
    )

    match len(chunks):
        case 0:
            return youtube_cheatsheet.exceptions.TranscriptSplitError()
        case 1:
            return [transcript]
        case _:
            return list(chunk for chunk in chunks)


def handle_result(result: Result[str, None], youtube_video: YouTube) -> str:
    """Processes the result of a transcript fetch."""
    match result:
        case Success():
            return result.unwrap()
        case Failure():
            print("No transcript found", file=stderr)
            return handle_transcript_generation(youtube_video, result)
        case _:
            raise NotImplementedError(f"Unhandled result: {result}")


def handle_transcript_generation(youtube_video: YouTube, result: Result) -> str:
    """Handles transcript generation in case of a fetch failure."""
    generate_result = youtube_cheatsheet.ai_providers.assemblyai.generate_transcript(
        youtube_video
    )
    if isinstance(generate_result, Failure):
        raise youtube_cheatsheet.exceptions.TranscriptGenerationFailedError(
            result.failure()
        )
    return generate_result.unwrap()


# def split_transcript(transcript: str) -> tuple[str, ...]:
#     """
#     Split a transcript into multiple parts.

#     """
#     result, value = youtube_cheatsheet.transcript.split(transcript)
#     if result == 1:
#         raise youtube_cheatsheet.exceptions.TranscriptSplitError()

#     return value
