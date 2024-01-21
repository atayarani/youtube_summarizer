import tempfile

import attrs
from attrs import define, field, frozen
from langchain_community.document_loaders import (
    AssemblyAIAudioTranscriptLoader,
    YoutubeLoader,
)
from pytube import YouTube
from youtube_transcript_api._errors import NoTranscriptFound


@frozen
class Metadata:
    """Represents the metadata of a transcript."""

    title: str = field(factory=str)
    publish_date: str = field(factory=str, metadata={"format": "%Y-%m-%d"})
    author: str = field(factory=str)
    url: str = field(factory=str)

    def __attrs_post_init__(self):
        """Post-initialization validation."""
        for key, value in attrs.asdict(self).items():
            if not value:
                raise ValueError(f"{key} cannot be empty.")
            if not isinstance(value, str):
                raise TypeError(f"{key} must be a string.")
            if len(value) == "":
                raise ValueError(f"{key} cannot be empty.")

    def print(self) -> str:
        """Prints the metadata information."""
        return (
            f"Title: {self.title}\n"
            f"Publish Date: {self.publish_date}\n"
            f"Author: {self.author}\n"
            f"URL: {self.url}\n"
        )


@define
class AssemblyTranscription:
    """
    Represents an Assembly AI transcription.

    Attributes:
        page_content (str): The content of the transcription page.
        metadata (dict): Additional metadata associated with the transcription.
    """

    page_content: str = field(factory=str)
    metadata: dict = field(factory=dict)


@frozen
class Transcript:
    """Represents a transcript."""

    content: str = field(factory=str)
    metadata: Metadata = field(factory=Metadata)

    @classmethod
    def get_transcript(cls, url: str) -> "Transcript":
        """
        Retrieves a transcript from the given URL.

        Args:
            url (str): The URL of the transcript.

        Returns:
            Transcript: The retrieved transcript.
        """
        if not Transcript.check_url(url):
            raise ValueError("Invalid YouTube URL")
        if not url:
            raise ValueError("URL cannot be empty")
        url = url.split("&")[0]
        loader = YoutubeLoader.from_youtube_url(
            url, add_video_info=True, language=["en", "en-US"]
        )
        try:
            output = loader.load()
            output = output[0]
        except NoTranscriptFound:
            output = cls._generate_transcript(url)
        except IndexError:
            raise ValueError("No transcript available")

        try:
            metadata = Metadata(
                title=output.metadata["title"],
                publish_date=output.metadata["publish_date"],
                author=output.metadata["author"],
                url=url.split("&")[0],
            )
        except Exception:
            print(output.metadata)

        return cls(content=output.page_content, metadata=metadata)

    @staticmethod
    def check_url(url: str) -> bool:
        """
        Check if the given URL is a valid YouTube video URL.

        Args:
            url (str): The URL to be checked.

        Returns:
            bool: True if the URL is a valid YouTube video URL, False otherwise.
        """
        return any(
            url.startswith(prefix)
            for prefix in [
                "https://www.youtube.com/watch?v=",
                "https://www.youtube.com/shorts",
            ]
        )

    @classmethod
    def _generate_transcript(cls, url: str) -> AssemblyTranscription:
        """
        Generate a transcript for a YouTube video given its URL.

        Args:
            url (str): The URL of the YouTube video.

        Returns:
            AssemblyTranscription: The generated transcript along with metadata.
        """
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        metadata = {
            "title": yt.title,
            "publish_date": yt.publish_date.strftime("%Y-%m-%d"),
            "author": yt.author,
        }

        with tempfile.TemporaryDirectory() as save_dir:
            audio_file = audio.download(output_path=save_dir)
            loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)
            docs = loader.load()
        return AssemblyTranscription(
            page_content=docs[0].page_content, metadata=metadata
        )
