import attrs
from attrs import field, frozen
from langchain_community.document_loaders import YoutubeLoader


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
        if not url.startswith("https://www.youtube.com/watch?v="):
            raise ValueError("Invalid YouTube URL")
        if not url:
            raise ValueError("URL cannot be empty")

        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        output = loader.load()
        if not output:
            raise Exception("No transcript available.")
        output = output[0]
        metadata = Metadata(
            title=output.metadata["title"],
            publish_date=output.metadata["publish_date"],
            author=output.metadata["author"],
            url=url.split("&")[0],
        )

        return cls(content=output.page_content, metadata=metadata)
