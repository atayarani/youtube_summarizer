import copy
from datetime import datetime

import pytube
import pytube.exceptions
from returns.maybe import Maybe, Nothing, Some

import youtube_cheatsheet.exceptions


class YouTubeData:
    def __init__(self) -> None:
        self.video: pytube.YouTube | None = None
        self._metadata: dict | None = None

    def get_from_url(self, url: str) -> pytube.YouTube:
        """Get a YouTube video object from the given URL."""

        try:
            video = pytube.YouTube(url.split("&")[0])
            video.check_availability()  # pragma: no cover
        except pytube.exceptions.RegexMatchError as err:
            raise youtube_cheatsheet.exceptions.InvalidURLError from err

        self.video = video
        return video

    @property
    def metadata(
        self,
    ) -> dict[str, str | None] | youtube_cheatsheet.exceptions.MissingMetadataError:
        video = self._validate_video()
        if video is None:
            return youtube_cheatsheet.exceptions.MissingMetadataError()

        video.streams.first()

        return {
            "title": video.title,
            "publish_date": self._format_publish_date(video.publish_date),
            "author": video.author,
            "url": video.watch_url,
            "description": self._format_description(video.description),
            "video_id": video.video_id,
        }

    def metadata_string(self, add_metadata: bool) -> str | None:
        metadata_info = self._validate_metadata()
        return (
            Maybe.from_optional(Some if add_metadata else Nothing)
            .from_optional(metadata_info)
            .bind_optional(lambda info: self._format_metadata(info))
            .value_or(None)
        )

    def _validate_video(self) -> pytube.YouTube | None:
        if self.video is None:
            return None
        if self.video.title is None:
            return None
        return copy.copy(self.video)

    def _validate_metadata(self) -> dict[str, str | None] | None:
        if isinstance(
            self.metadata, youtube_cheatsheet.exceptions.MissingMetadataError
        ):
            return None
        return self.metadata

    @staticmethod
    def _format_metadata(info: dict[str, str | None]) -> str:
        return "\n".join([f"{k}: {v}" for k, v in info.items() if k != "video_id"])  # type:ignore

    # @staticmethod
    def _format_publish_date(self, publish_date: datetime | None) -> str | None:
        return (
            Maybe.from_optional(publish_date)
            .bind_optional(lambda date: date.strftime("%Y-%m-%d"))
            .value_or(None)
        )

    @staticmethod
    def _format_description(description: str) -> str:
        return "".join([f"\n\t{x}" for x in description.split("\n")])
