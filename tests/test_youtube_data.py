import pytest
import pytube

from src.youtube_data import get_youtube_data_from_url


@pytest.fixture()
def url():
    """
    Returns the method URL.

    :returns: The method URL.

    Example:
    :rtype: str

    >>> url()
        'https://www.youtube.com/watch?v=12345'
    """
    return "https://www.youtube.com/watch?v=12345"


def test_get_youtube_data_from_url_success(mocker, url):
    """
    Test the get_youtube_data_from_url function.

    :param mocker: The mocker object used for mocking pytube
    :param url: The YouTube URL from which to fetch data

    Example Usage:
    mocker = pytest.mock.Mock()
    test_get_youtube_data_from_url_success(mocker, "https://www.youtube.com/watch?v=VIDEO_ID")

    """
    mock_video = mocker.patch("pytube.YouTube")
    mock_avail = mock_video.return_value.check_availability

    result, value = get_youtube_data_from_url(url)

    assert result == 0
    assert value == mock_video.return_value
    mock_avail.assert_called_once()


def test_get_youtube_data_from_url_fail(mocker, url):
    """
    Test the get_youtube_data_from_url function.

    :param mocker: The mocker object used for mocking pytube
    :param url: The YouTube URL from which to fetch data

    Example Usage:
    mocker = pytest.mock.Mock()
    test_get_youtube_data_from_url_fail(mocker, "https://www.youtube.com/watch?v=VIDEO_ID")

    """
    mock_video = mocker.patch("pytube.YouTube")
    mock_video.side_effect = pytube.exceptions.RegexMatchError(
        "video_id", r"watch\?v=\S+"
    )

    result, value = get_youtube_data_from_url(url)

    assert result == 1
    assert value == "Invalid YouTube URL"
