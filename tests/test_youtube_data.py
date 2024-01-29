import pytest
from pytube.exceptions import RegexMatchError
from typer import BadParameter

from src.metadata import Metadata
from src.youtube_data import YouTubeData


@pytest.fixture
def valid_metadata():
    return Metadata(
        title="Title",
        publish_date="2022-01-01",
        author="Author",
        url="www.example.com",
        description="Description",
        video_id="12345",
    )


@pytest.fixture
def mock_youtube_data__get_video(mocker):
    return mocker.patch("src.youtube_data.YouTubeData._get_video")


@pytest.fixture
def mock_youtube_data(mocker):
    return mocker.patch("src.youtube_data.YouTubeData")


class TestYoutubeData:
    def test_youtube_data_metadata(self, valid_metadata, mock_youtube_data__get_video):
        video = mock_youtube_data__get_video.return_value
        video.title = valid_metadata.title
        video.publish_date.strftime.return_value = valid_metadata.publish_date
        video.author = valid_metadata.author
        video.watch_url = valid_metadata.url
        video.description = valid_metadata.description
        video.video_id = valid_metadata.video_id

        youtube_data = YouTubeData("https://www.youtube.com/watch?v=12345")
        metadata = youtube_data.metadata
        assert metadata.title == valid_metadata.title
        assert metadata.publish_date == valid_metadata.publish_date
        assert metadata.author == valid_metadata.author
        assert metadata.url == valid_metadata.url
        assert metadata.description == f"\n\t{valid_metadata.description}"
        assert metadata.video_id == valid_metadata.video_id

    def test_youtube_data__get_video_raises_error(self, mock_youtube_data__get_video):
        mock_youtube_data__get_video.side_effect = BadParameter("Invalid YouTube URL")
        with pytest.raises(BadParameter):
            YouTubeData("https://www.youtube.com/watch?v=12345")

    # @FIXME: This test fails
    # pytube.Youtube doesn't mock properly
    # def test_youtube_data__get_video_returns_youtube_object(self, mocker):
    #     mock_youtube = mocker.patch("pytube.YouTube")
    #     mock_availability = mocker.patch("pytube.YouTube.check_availability")
    #     youtube = YouTubeData("https://www.youtube.com/watch?v=12345")

    #     assert youtube.video == mock_youtube
