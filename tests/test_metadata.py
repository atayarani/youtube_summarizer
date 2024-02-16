from types import MappingProxyType

from src.metadata import set_metadata


class TestSetMetadata:
    """
    This class provides functionality to set metadata for a YouTube video.

    Methods:
        test_set_metadata

    """

    def test_set_metadata(self, mocker) -> None:
        """
        set_metadata method sets the metadata for a YouTube video.

        Args:
            mocker: The mocker object for creating patches and mocks.

        Returns:
            MappingProxyType: A read-only proxy object representing the video metadata.

        Example usage:
            mock_youtube_video = mocker.patch("pytube.YouTube")
            mock_youtube_video.streams.first.return_value = None
            mock_youtube_video.title = "Title"
            mock_youtube_video.publish_date.strftime.return_value = "2022-01-01"
            mock_youtube_video.author = "Author"
            mock_youtube_video.watch_url = "www.example.com"
            mock_youtube_video.description = "Description"
            mock_youtube_video.video_id = "12345"

            metadata = set_metadata(mock_youtube_video)

            mock_youtube_video.streams.first.assert_called_once()
            assert isinstance(metadata, MappingProxyType)
        """
        mock_youtube_video = mocker.patch("pytube.YouTube")
        mock_youtube_video.streams.first.return_value = None
        mock_youtube_video.title = "Title"
        mock_youtube_video.publish_date.strftime.return_value = "2022-01-01"
        mock_youtube_video.author = "Author"
        mock_youtube_video.watch_url = "www.example.com"
        mock_youtube_video.description = "Description"
        mock_youtube_video.video_id = "12345"

        metadata = set_metadata(mock_youtube_video)

        mock_youtube_video.streams.first.assert_called_once()
        assert isinstance(metadata, MappingProxyType)
