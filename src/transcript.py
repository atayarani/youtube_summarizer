import tempfile
from functools import lru_cache

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

from src.youtube_data import YouTubeData


class Transcript:
    def __init__(self, youtube_data: YouTubeData):
        self.content = self.get_transcript(youtube_data)

    @lru_cache
    def get_transcript(self, data: YouTubeData) -> str:
        video_id = data.video.video_id
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([item["text"] for item in transcript])
        except NoTranscriptFound:
            return self.generate(data)
        except TranscriptsDisabled:
            return self.generate(data)

    @lru_cache
    def split(self) -> list[str]:
        """Split the transcript into chunks using a character-based text splitter.

        Returns:
            A list of transcript chunks.
        """
        transcript_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=10000, chunk_overlap=0
        )

        chunks = transcript_splitter.split_text(self.content)
        if len(chunks) == 0:
            raise Transcript.InvalidTranscript()

        return chunks

    def generate(self, data: YouTubeData) -> str:
        """
        Generate a transcript for a YouTube video given its URL.

        Args:
            url (str): The URL of the YouTube video.

        Returns:
            AssemblyTranscription: The generated transcript along with metadata.
        """
        yt = data.video
        audio = yt.streams.filter(only_audio=True).first()

        with tempfile.TemporaryDirectory() as save_dir:
            audio_file = audio.download(output_path=save_dir)
            loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)
            docs = loader.load()
        return docs[0].page_content

    class InvalidTranscript(ValueError):
        """Raised when the transcript is not specified."""

        def __init__(self) -> None:
            """Initializes the InvalidTranscript exception."""
            super().__init__("The transcript must be specified.")
