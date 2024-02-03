import tempfile
from typing import Tuple

import langchain
import youtube_transcript_api
from langchain.docstore.document import Document
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from pytube import YouTube


def get_transcript(video_id: str) -> Tuple[int, str]:
    try:
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(
            video_id
        )
        return (0, " ".join([item["text"] for item in transcript]))
    except youtube_transcript_api._errors.NoTranscriptFound as err:
        return (1, err.CAUSE_MESSAGE)
    except youtube_transcript_api._errors.TranscriptsDisabled as err:
        return (2, err.CAUSE_MESSAGE)


def generate_transcript(video: YouTube) -> Tuple[int, str]:
    """
    Generate a transcript for a YouTube video given its URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        AssemblyTranscription: The generated transcript along with metadata.
    """

    with tempfile.TemporaryDirectory() as save_dir:
        audio_file = fetch_youtube_audio(video, save_dir)
        transcript = parse_youtube_audio(audio_file)
    if len(transcript) == 0:
        return (1, "No transcript found")

    return (0, transcript[0].page_content)


def split(transcript: str) -> Tuple[int, Tuple[str, ...]]:
    transcript_splitter = langchain.text_splitter.CharacterTextSplitter.from_tiktoken_encoder(
        # chunk_size=10, chunk_overlap=0
        chunk_size=10000,
        chunk_overlap=0,
    )
    # print(transcript_splitter)

    chunks = transcript_splitter.split_text(transcript)
    # print(len(chunks))
    if len(chunks) == 1:
        return (0, (transcript,))
    if len(chunks) == 0:
        return (1, ("The transcript must be specified.",))

    return (0, tuple(chunk for chunk in chunks))


def fetch_youtube_audio(video: YouTube, save_dir: str) -> YouTube:
    audio = video.streams.filter(only_audio=True).first()  # pragma: no cover
    return audio.download(output_path=save_dir)  # pragma: no cover


def parse_youtube_audio(audio_file: str) -> list[Document]:
    loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)  # pragma: no cover
    return loader.load()  # pragma: no cover
