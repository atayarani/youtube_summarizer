import tempfile

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled


def get_transcript(video_id: str) -> tuple[int, str]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return (0, " ".join([item["text"] for item in transcript]))
    except NoTranscriptFound:
        return (1, "No transcript found")
        # return self.generate(data)
    except TranscriptsDisabled:
        return (2, "Transcripts disabled")
        # return self.generate(data)


def generate_transcript(video: YouTube) -> str:
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
    content: str = transcript[0].page_content
    return content


def split(transcript: str) -> tuple[int, list[str] | str]:
    transcript_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=10000, chunk_overlap=0
    )

    chunks = transcript_splitter.split_text(transcript)
    if len(chunks) == 0:
        return (1, "The transcript must be specified.")

    return (0, chunks)


def fetch_youtube_audio(video: YouTube, save_dir: str) -> YouTube:
    audio = video.streams.filter(only_audio=True).first()
    return audio.download(output_path=save_dir)


def parse_youtube_audio(audio_file: str) -> list:  # type: ignore
    loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)
    return loader.load()


# class Transcript:
# def __init__(self, youtube_data: YouTubeData):
# self.content = self.get_transcript(youtube_data)

# @lru_cache
# def get_transcript(self, data: YouTubeData) -> str:
#         """
#         Retrieves the transcript of a YouTube video.

#         Args:
#             data (YouTubeData): The YouTube data object containing the video information.

#         Returns:
#             str: The transcript of the YouTube video.
#         """
#         video_id = data.video.video_id
#         try:
#             transcript = YouTubeTranscriptApi.get_transcript(video_id)
#             return " ".join([item["text"] for item in transcript])
#         except NoTranscriptFound:
#             return self.generate(data)
#         except TranscriptsDisabled:
#             return self.generate(data)

# @lru_cache
# def generate(self, data: YouTubeData) -> str:
#     """
#     Generate a transcript for a YouTube video given its URL.

#     Args:
#         url (str): The URL of the YouTube video.

#     Returns:
#         AssemblyTranscription: The generated transcript along with metadata.
#     """
#     yt = data.video
#     audio = yt.streams.filter(only_audio=True).first()

#     with tempfile.TemporaryDirectory() as save_dir:
#         audio_file = audio.download(output_path=save_dir)
#         loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)
#         docs = loader.load()
#     return docs[0].page_content

# class InvalidTranscript(ValueError):
#     """Raised when the transcript is not specified."""

#     def __init__(self) -> None:
#         """Initializes the InvalidTranscript exception."""
#         super().__init__()
