import pytest

import src.cli


@pytest.fixture
def url():
    return "https://www.youtube.com/watch?v=12345"


def test_function_succeeds(mocker, url):
    youtube_data = mocker.patch("src.youtube_data.get_youtube_data_from_url")
    value = "return value"
    youtube_data.return_value = (0, value)
    assert src.cli.get_youtube_data_from_url(url) == value


def test_function_fails(mocker, url):
    youtube_data = mocker.patch("src.youtube_data.get_youtube_data_from_url")
    value = "return value"
    youtube_data.return_value = (1, value)
    with pytest.raises(ValueError):
        src.cli.get_youtube_data_from_url(url)
