import tempfile

import youtube_transcript_api
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from pytube import YouTube
from returns.result import Failure, Result, Success, safe


@safe(
    exceptions=(
        youtube_transcript_api._errors.NoTranscriptFound,
        youtube_transcript_api._errors.TranscriptsDisabled,
        youtube_transcript_api._errors.NoTranscriptAvailable,
    )
)
def get_transcript(video_id: str) -> str:
    """
    Get the transcript for a given YouTube video.

    Args:
        video_id (str): The ID of the YouTube video for which the transcript is requested.

    Returns:
        str: The concatenated transcript of the video, converted from a list of transcript items.

    Raises:
        youtube_transcript_api._errors.NoTranscriptFound: If no transcript is found for the video.
        youtube_transcript_api._errors.TranscriptsDisabled: If transcripts are disabled for the video.
        youtube_transcript_api._errors.NoTranscriptAvailable: If no transcript is available for the video.

    """
    transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([item["text"] for item in transcript])


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
