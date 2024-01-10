from dataclasses import dataclass

from langchain_community.document_loaders import YoutubeLoader


@dataclass
class Metadata:
    title: str
    publish_date: str
    author: str
    url: str

    def print(self) -> None:
        print(f"Title: {self.title}")
        print(f"Publish Date: {self.publish_date}")
        print(f"Author: {self.author}")
        print(f"URL: {self.url}")


@dataclass
class Transcript:
    content: str
    metadata: Metadata

    @classmethod
    def get_transcript(cls, url: str) -> "Transcript":
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        output = loader.load()[0]
        metadata = Metadata(
            title=output.metadata["title"],
            publish_date=output.metadata["publish_date"],
            author=output.metadata["author"],
            url=url,
        )

        return cls(content=output.page_content, metadata=metadata)
