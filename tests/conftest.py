import pytest
import youtube_cheatsheet.video_providers.youtube.data
from pytest_mock import MockerFixture
from typer.testing import CliRunner


# Add any fixtures, plugins or command line options here
@pytest.fixture()
def mock_youtube_data(mocker: MockerFixture) -> MockerFixture:
    return mocker.Mock(
        spec=youtube_cheatsheet.video_providers.youtube.data.YouTubeData()
    )


@pytest.fixture()
def runner():
    return CliRunner()
