from dataclasses import dataclass

from langchain_community.document_loaders import YoutubeLoader


@dataclass
class Metadata:
    """Represents the metadata of a transcript."""

    title: str
    publish_date: str
    author: str
    url: str

    def print(self) -> str:
        """Prints the metadata information."""
        return (
            f"Title: {self.title}\n"
            f"Publish Date: {self.publish_date}\n"
            f"Author: {self.author}\n"
            f"URL: {self.url}\n"
        )


@dataclass
class Transcript:
    """Represents a transcript."""

    content: str
    metadata: Metadata

    @classmethod
    def get_transcript(cls, url: str) -> "Transcript":
        """
        Retrieves a transcript from the given URL.

        Args:
            url (str): The URL of the transcript.

        Returns:
            Transcript: The retrieved transcript.
        """
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        output = loader.load()[0]
        metadata = Metadata(
            title=output.metadata["title"],
            publish_date=output.metadata["publish_date"],
            author=output.metadata["author"],
            url=url,
        )

        return cls(content=output.page_content, metadata=metadata)
