import tempfile

import youtube_transcript_api
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from pytube import YouTube
from returns.maybe import Maybe
from returns.result import Failure, Result, Success
from toolz import functoolz


def get_transcript(video_id: str) -> str | None:
    safe_function = functoolz.excepts(
        (
            youtube_transcript_api._errors.NoTranscriptFound,
            youtube_transcript_api._errors.TranscriptsDisabled,
            youtube_transcript_api._errors.NoTranscriptAvailable,
        ),
        lambda id: youtube_transcript_api.YouTubeTranscriptApi.get_transcript(id),
        lambda _: None,
    )

    return (
        Maybe.from_optional(safe_function(video_id))
        .bind_optional(lambda transcript: " ".join(format_transcript(transcript)))
        .value_or(None)
    )


def format_transcript(transcript: dict) -> list[str]:
    return [item["text"] for item in transcript]


def generate_transcript(video: YouTube) -> Result[str, None]:
    """
    Generate a transcript for a given YouTube video.

    Args:
        video: A YouTube object representing the video from which the transcript will be generated.

    Returns:
        A Result object containing the transcript as a string if successful, or None if unsuccessful.

    Raises:
        None

    """
    with tempfile.TemporaryDirectory() as save_dir:
        audio_file: str = fetch_youtube_audio(video, save_dir)
        transcript = parse_youtube_audio(audio_file)

    if len(transcript) == 0:
        return Failure(None)

    return Success(transcript[0].page_content)


def split(transcript: str) -> tuple[int, tuple[str, ...]]:
    """
    Split a transcript into chunks based on langchain splitter.

    Args:
        transcript (str): The transcript to be split into chunks.

    Returns:
        Tuple[int, Tuple[str,...]]: A tuple containing an integer status code and a tuple of chunks.

        The status code indicates the success or failure of the splitting operation:
            - 0: Splitting successful.
            - 1: The transcript must be specified.

        The chunks tuple contains the resulting chunks after splitting the transcript.
        Each chunk is a string.

    Example:
        >>> transcript = "This is a sample transcript."
        >>> split(transcript)
        (0, ('This is a sample transcript.',))

        >>> transcript = ""
        >>> split(transcript)
        (1, ('The transcript must be specified.',))

    """
    transcript_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=10000,
        chunk_overlap=0,
    )

    chunks = transcript_splitter.split_text(transcript)
    if len(chunks) == 1:
        return 0, (transcript,)
    if len(chunks) == 0:
        return 1, ("The transcript must be specified.",)

    return 0, tuple(chunk for chunk in chunks)


def fetch_youtube_audio(video: YouTube, save_dir: str) -> str:
    """
    Fetch the audio file for a given YouTube video.

    Args:
        video: A YouTube object representing the video from which audio needs to be fetched.
        save_dir: A string representing the directory path where the audio file will be saved.

    Returns:
        A string representing the file path of the downloaded audio file.

    """
    audio = video.streams.filter(only_audio=True).first()  # pragma: no cover
    return str(audio.download(output_path=save_dir))  # pragma: no cover


def parse_youtube_audio(audio_file: str) -> list[Document]:
    """
    Parse the audio file for a given YouTube video.

    Args:
        audio_file: A string representing the file path of the audio file.

    Returns:
        A list of Document objects representing the transcripts of the audio file.
    """
    loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)  # pragma: no cover
    return loader.load()  # pragma: no cover


# def get_transcript(youtube_video: YouTube) -> str:
#     """Retrieve the transcript for a given YouTube video."""
#     result = fetch_transcript(youtube_video)
#     return handle_result(result, youtube_video)


# def fetch_transcript(youtube_video: YouTube) -> Result:
#     return maybe_to_result(Maybe.from_optional(get_transcript(youtube_video.video_id)))


# def handle_result(result: Result, youtube_video: YouTube) -> str:
#     """Processes the result of a transcript fetch."""
#     if not isinstance(result, Success | Failure):
#         raise NotImplementedError(f"Unhandled result: {result}")

#     if isinstance(result, Failure):
#         print("No transcript found", file=stderr)
#         return handle_transcript_generation(youtube_video, result)
#     return result.unwrap()


# def handle_transcript_generation(youtube_video: YouTube, result: Result) -> str:
#     """Handles transcript generation in case of a fetch failure."""
#     generate_result = youtube_cheatsheet.transcript.generate_transcript(youtube_video)
#     if isinstance(generate_result, Failure):
#         raise youtube_cheatsheet.exceptions.TranscriptGenerationFailedError(
#             result.failure()
#         )
#     return generate_result.unwrap()


# def split_transcript(transcript: str) -> tuple[str, ...]:
#     """
#     Split a transcript into multiple parts.

#     :param transcript: str:
#     :type transcript: str
#     :param transcript: str:
#     :param transcript: str:
#     :returns: A tuple containing the split parts of the
#     :rtype: Tuple[str, ...]
#     :raises ValueError: If the split operation fails.

#     Example:
#     >>> transcript = "This is a transcript"
#         >>> split_transcript(transcript)
#         ("This is a transcript",)
#     """
#     result, value = youtube_cheatsheet.transcript.split(transcript)
#     if result == 1:
#         raise ValueError(value)

#     return value
