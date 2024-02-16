import pytest

import src.cli


@pytest.fixture()
def url():
    """
    Return the URL for a given resource.

    Args:
        None

    Returns:
        str: The URL of the resource.

    Example:
        >>> url()
        "https://www.youtube.com/watch?v=12345"
    """
    return "https://www.youtube.com/watch?v=12345"


def test_function_succeeds(mocker, url):
    """
    Test that the function succeeds by mocking the YouTube data and validating the returned value.

    Args:
        mocker: An instance of the mocker object, used for patching the 'get_youtube_data_from_url' method.
        url (str): The URL for the YouTube video.

    Returns:
        None
    """
    youtube_data = mocker.patch("src.youtube_data.get_youtube_data_from_url")
    value = "return value"
    youtube_data.return_value = (0, value)
    assert src.cli.get_youtube_data_from_url(url) == value


def test_function_fails(mocker, url):
    """
    Test that the function fails by mocking the YouTube data and validating the returned value.

    Args:
        mocker: The mocker object used for mocking the "get_youtube_data_from_url" function.
        url: The URL to pass to the "get_youtube_data_from_url" function.

    Raises:
        ValueError: If the "get_youtube_data_from_url" function does not raise a ValueError.

    """
    youtube_data = mocker.patch("src.youtube_data.get_youtube_data_from_url")
    value = "return value"
    youtube_data.return_value = (1, value)
    with pytest.raises(ValueError):
        src.cli.get_youtube_data_from_url(url)
