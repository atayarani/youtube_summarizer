"""
This module provides functionality for fetching and processing data from YouTube.
It utilizes the `pytube` library to interact with the YouTube API and retrieve video information.
The main class in this module is `YouTubeData`, which allows users to fetch video metadata and descriptions.
"""

from functools import lru_cache

from pytube import YouTube
from pytube.exceptions import RegexMatchError
from typer import BadParameter

from src.metadata import Metadata


class YouTubeData:
    def __init__(self, url: str):
        """
        Initialize the object with the given URL.

        Args:
            url (str): The URL of the video.
        """
        self._url = url
        self.video: YouTube = self._get_video()

    @property
    def url(self) -> str:
        return self._url

    @property
    def metadata(self) -> Metadata:
        return Metadata(
            title=self.video.title,
            publish_date=self.video.publish_date.strftime("%Y-%m-%d"),
            author=self.video.author,
            url=self.video.watch_url,
            description=self.description,
            video_id=self.video.video_id,
        )

    @lru_cache
    def _get_video(self) -> YouTube:
        """
        Set the video property with the given URL.

        Args:
            url (str): The URL of the video.

        Returns:
            YouTube: The YouTube object representing the video.

        Raises:
            RegexMatchError: If the URL does not match the expected format.
        """
        try:
            video = YouTube(self.url)
            video.check_availability()  # pragma: no cover
        except RegexMatchError:
            raise BadParameter("Invalid YouTube URL")

        return video

    @property
    def description(self) -> str:
        """
        Get the description of the video as a single string.
        """
        self.video.streams.first()
        return "".join([f"\n\t{x}" for x in self.video.description.split("\n")])
