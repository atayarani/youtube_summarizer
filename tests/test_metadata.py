from types import MappingProxyType

import pytest

from src.metadata import set_metadata


class TestSetMetadata:
    def test_set_metadata(self, mocker):
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


# from src.metadata import Metadata


# @pytest.fixture
# def valid_metadata():
#     return Metadata(
#         title="Title",
#         publish_date="2022-01-01",
#         author="Author",
#         url="www.example.com",
#         description="Description",
#         video_id="12345",
#     )


# @pytest.fixture
# def valid_output():
#     return "Title: Title\nPublish Date: 2022-01-01\nAuthor: Author\nURL: www.example.com\nDescription: Description\n"


# class TestMetadata:
#     def test_returns_metadata_as_string(self, valid_metadata, valid_output):
#         metadata = valid_metadata
#         expected_output = valid_output
#         assert str(metadata) == expected_output
