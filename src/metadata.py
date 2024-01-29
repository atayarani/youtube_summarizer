from attrs import field, frozen, validators


def metadata_validators() -> list:  # type: ignore
    return [
        validators.instance_of(str),
        validators.min_len(1),
    ]


@frozen
class Metadata:
    """Represents the metadata of a transcript."""

    title: str = field(factory=str, validator=metadata_validators())
    publish_date: str = field(
        factory=str, metadata={"format": "%Y-%m-%d"}, validator=metadata_validators()
    )
    author: str = field(factory=str, validator=metadata_validators())
    url: str = field(factory=str, validator=metadata_validators())
    description: str = field(factory=str, validator=metadata_validators())
    video_id: str = field(factory=str, validator=metadata_validators())

    def __str__(self) -> str:
        """Returns the metadata information as a formatted string."""

        return (
            f"Title: {self.title}\n"
            f"Publish Date: {self.publish_date}\n"
            f"Author: {self.author}\n"
            f"URL: {self.url}\n"
            f"Description: {self.description}\n"
        )
