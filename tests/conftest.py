import pytest
import youtube_cheatsheet.youtube_data
from pytest_mock import MockerFixture


# Add any fixtures, plugins or command line options here
@pytest.fixture()
def mock_youtube_data(mocker: MockerFixture) -> MockerFixture:
    return mocker.Mock(spec=youtube_cheatsheet.youtube_data.YouTubeData())
