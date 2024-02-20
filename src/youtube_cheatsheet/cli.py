import pathlib
from sys import stderr
from typing import Annotated, Optional

import typer
from pytube import YouTube
from returns.converters import maybe_to_result
from returns.maybe import Maybe
from returns.pipeline import flow
from returns.result import Failure, Result, Success

import youtube_cheatsheet.ai_providers.openai
import youtube_cheatsheet.exceptions
import youtube_cheatsheet.metadata
import youtube_cheatsheet.output
import youtube_cheatsheet.transcript
import youtube_cheatsheet.youtube_data

app: typer.Typer = typer.Typer(
    help="AI Assistant for YouTube videos", rich_markup_mode="rich"
)


@app.command()
def main(
    url: Annotated[str, typer.Argument(help="The URL of the YouTube video")],
    takeaways: Annotated[
        bool, typer.Option(help="Whether or not to include key takeaways")
    ] = True,
    summary: Annotated[
        bool, typer.Option(help="Whether or not to include an article summary")
    ] = True,
    metadata: Annotated[
        bool, typer.Option(help="Whether or not to include video metadata")
    ] = True,
    path: Annotated[
        Optional[pathlib.Path],
        typer.Option(help="The path to write the output file to"),
    ] = None,
) -> None:
    """
    Process YouTube videos and write the output to a file or stdout.
    """
    youtube_video = youtube_cheatsheet.youtube_data.YouTubeData()
    transcript_chunks = flow(
        youtube_video.get_from_url(url), get_transcript, split_transcript
    )
    metadata_info = youtube_video.metadata
    if isinstance(metadata_info, youtube_cheatsheet.exceptions.MissingMetadataError):
        print(repr(metadata_info))
        exit(1)

    # We pass the boolean values to the methods here, so we don't generate them
    # if the template doesn't need them.  If we do it in the template, which
    # was my original plan, then we may generate data from AI providers for
    # no good reason.
    output = youtube_cheatsheet.output.get_output(
        metadata_info["title"],  # type: ignore
        youtube_data_metadata=youtube_video.metadata_string(metadata),
        output_takeaways=youtube_cheatsheet.ai_providers.openai.get_takeaways(
            takeaways, transcript_chunks
        ),
        output_summary=youtube_cheatsheet.ai_providers.openai.get_summary(
            summary, transcript_chunks
        ),
    )

    youtube_cheatsheet.output.write_file(
        metadata_info["title"],
        output,
        path,  # type: ignore
    ) if path else print(output)


def get_transcript(youtube_video: YouTube) -> str:
    """Retrieve the transcript for a given YouTube video."""
    result = fetch_transcript(youtube_video)
    return handle_result(result, youtube_video)


def fetch_transcript(youtube_video: YouTube) -> Result:
    """Fetches the transcript and returns the result."""
    return maybe_to_result(
        Maybe.from_optional(
            youtube_cheatsheet.transcript.get_transcript(youtube_video.video_id)
        )
    )


def handle_result(result: Result, youtube_video: YouTube) -> str:
    """Processes the result of a transcript fetch."""
    if not isinstance(result, Success | Failure):
        raise NotImplementedError(f"Unhandled result: {result}")

    if isinstance(result, Failure):
        print("No transcript found", file=stderr)
        return handle_transcript_generation(youtube_video, result)
    return result.unwrap()


def handle_transcript_generation(youtube_video: YouTube, result: Result) -> str:
    """Handles transcript generation in case of a fetch failure."""
    generate_result = youtube_cheatsheet.transcript.generate_transcript(youtube_video)
    if isinstance(generate_result, Failure):
        raise youtube_cheatsheet.exceptions.TranscriptGenerationFailedError(
            result.failure()
        )
    return generate_result.unwrap()


def split_transcript(transcript: str) -> tuple[str, ...]:
    """
    Split a transcript into multiple parts.

    :param transcript: str:
    :type transcript: str
    :param transcript: str:
    :param transcript: str:
    :returns: A tuple containing the split parts of the
    :rtype: Tuple[str, ...]
    :raises ValueError: If the split operation fails.

    Example:
    >>> transcript = "This is a transcript"
        >>> split_transcript(transcript)
        ("This is a transcript",)
    """
    result, value = youtube_cheatsheet.transcript.split(transcript)
    if result == 1:
        raise ValueError(value)

    return value


if __name__ == "__main__":
    ...
