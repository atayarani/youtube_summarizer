import pytest
import pytube

import src.youtube_data
from src.youtube_data import get_youtube_data_from_url


@pytest.fixture
def url():
    return "https://www.youtube.com/watch?v=12345"


def test_get_youtube_data_from_url_success(mocker, url):
    mock_video = mocker.patch("pytube.YouTube")
    mock_avail = mock_video.return_value.check_availability

    result, value = get_youtube_data_from_url(url)

    assert result == 0
    assert value == mock_video.return_value
    mock_avail.assert_called_once()


def test_get_youtube_data_from_url_fail(mocker, url):
    mock_video = mocker.patch("pytube.YouTube")
    mock_video.side_effect = pytube.exceptions.RegexMatchError(
        "video_id", r"watch\?v=\S+"
    )

    result, value = get_youtube_data_from_url(url)

    assert result == 1
    assert value == "Invalid YouTube URL"
