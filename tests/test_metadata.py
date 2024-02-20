# from types import MappingProxyType

# import pytest
# import youtube_cheatsheet.metadata
# from youtube_cheatsheet.metadata import set_metadata


# @pytest.fixture()
# def mock_data(mocker):
#     mock_youtube_video = mocker.patch("pytube.YouTube")
#     mock_youtube_video.streams.first.return_value = None
#     mock_youtube_video.title = "Title"
#     mock_youtube_video.publish_date.strftime.return_value = "2022-01-01"
#     mock_youtube_video.author = "Author"
#     mock_youtube_video.watch_url = "www.example.com"
#     mock_youtube_video.description = "Description"
#     mock_youtube_video.video_id = "12345"

#     return mock_youtube_video


# @pytest.fixture()
# def mock_mapping_proxy_data():
#     return MappingProxyType(
#         {
#             "title": "Title",
#             "author": "Author",
#             "description": "Description",
#         }
#     )


# class TestSetMetadata:
#     def test_set_metadata(self, mock_data) -> None:
#         metadata = set_metadata(mock_data)

#         mock_data.streams.first.assert_called_once()
#         assert isinstance(metadata, MappingProxyType)

#     def test_metadata_string(self, mock_mapping_proxy_data) -> None:
#         metadata_info = youtube_cheatsheet.metadata.metadata_string(
#             mock_mapping_proxy_data
#         )
#         assert isinstance(metadata_info, str)
