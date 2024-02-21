from datetime import datetime
import pytest
import pytube
from youtube_cheatsheet import youtube_data
import youtube_cheatsheet.exceptions
from youtube_cheatsheet.youtube_data import YouTubeData


@pytest.fixture()
def valid_url(mock_valid_video_object):
    return mock_valid_video_object.watch_url


@pytest.fixture()
def invalid_url():
    return "https://www.youtube.com/watch?v=foo"


@pytest.fixture()
def mock_valid_video_object(mocker):
    mock_video = mocker.Mock(spec=pytube.YouTube)
    mock_video.title = "Test Title"
    mock_video.publish_date = datetime(2022, 1, 1)
    mock_video.author = "Test Author"
    mock_video.watch_url = "https://www.youtube.com/watch?v=12345"
    mock_video.description = "Test Description"
    mock_video.video_id = "12345"

    return mock_video

class TestGetFromURL:

    def test_valid_url_returns_youtube_object(self, mocker, valid_url):
        """Return a pytube.YouTube object when given a valid URL."""
        youtube_data = YouTubeData()
        mocker.patch("pytube.YouTube", return_value=mocker.MagicMock())
        video = youtube_data.get_from_url(valid_url)
        assert isinstance(video, mocker.MagicMock)


    def test_invalid_url_raises_invalid_url_error(self, invalid_url):
        """Raise an InvalidURLError when given an invalid URL."""
        youtube_data = YouTubeData()
        with pytest.raises(youtube_cheatsheet.exceptions.InvalidURLError):
            youtube_data.get_from_url(invalid_url)


class TestMetadataProperty:
    def test_valid_video_metadata(self, mocker, mock_valid_video_object):
        # Initialize the YouTubeData object
        youtube_data = YouTubeData()
        expected_keys = [
            "title",
            "publish_date",
            "author",
            "url",
            "description",
            "video_id",
        ]
        mocker.patch.object(
            youtube_data, "_validate_video", return_value=mock_valid_video_object
        )

        metadata = youtube_data.metadata

        assert isinstance(metadata, dict)
        assert all(key in metadata for key in expected_keys)


    def test_missing_metadata_error_when_video_is_none(self,mocker):
        youtube_data = YouTubeData()
        mocker.patch.object(youtube_data, "_validate_video", return_value=None)

        assert isinstance(
            youtube_data.metadata, youtube_cheatsheet.exceptions.MissingMetadataError
        )

class TestMetadataString:
    def test_metadata_string_success(self,mocker, mock_valid_video_object):
        youtube_data = YouTubeData()
        mocker.patch.object(
            youtube_data, "_validate_video", return_value=mock_valid_video_object
        )

        youtube_data.metadata
        metadata_string = youtube_data.metadata_string(True)
        assert isinstance(metadata_string, str)

    def test_metadata_string_failure(self,mocker):
        youtube_data = YouTubeData()
        mocker.patch.object(
            youtube_data, "_validate_video", return_value=None
        )

        youtube_data.metadata
        metadata_string = youtube_data.metadata_string(True)
        assert metadata_string is None

class TestValidateVideo:
    def test_validate_video_video_none(self):
        youtube_data = YouTubeData()
        youtube_data.video = None

        assert youtube_data._validate_video() is None

    def test_validate_video_video_title_none(self, mock_valid_video_object):
        youtube_data = YouTubeData()
        youtube_data.video = mock_valid_video_object
        youtube_data.video.title = None
        assert youtube_data._validate_video() is None
    
    def test_validate_video_return_video_object(self, mocker, mock_valid_video_object):
        youtube_data = YouTubeData()
        youtube_data.video = mock_valid_video_object
        assert isinstance(youtube_data._validate_video(), pytube.YouTube)
