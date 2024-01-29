import os

import pytest
from typer import BadParameter
from typer.testing import CliRunner

from src.cli import app, get_youtube_data, slugify_video_title, write_file
from src.metadata import Metadata


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_application_runner(mocker):
    return mocker.patch("src.main.ApplicationRunner.run")


@pytest.fixture
def mock_youtube_data__get_video(mocker):
    return mocker.patch("src.youtube_data.YouTubeData._get_video")


@pytest.fixture
def mock_ai(mocker):
    return mocker.patch("src.ai.AI.__init__")


@pytest.fixture
def mock_ai_summary(mocker):
    return mocker.patch("src.ai.AI.summary")


@pytest.fixture
def valid_url():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@pytest.fixture
def mock_transcript_split(mocker):
    return mocker.patch("src.transcript.Transcript.split")


@pytest.fixture
def mock_youtube_metadata(mocker):
    return mocker.patch("src.youtube_data.YouTubeData.metadata")


@pytest.fixture
def mock_ai_takeaways(mocker):
    return mocker.patch("src.ai.AI.takeaways")


@pytest.fixture
def mock_transcript_get_transcript(mocker):
    return mocker.patch("src.transcript.Transcript.get_transcript")


@pytest.fixture
def mock_metadata():
    return Metadata(
        title="This is a Test Video",
        publish_date="2022-01-01",
        author="Author",
        url="www.example.com",
        description="Description",
        video_id="12345",
    )


@pytest.fixture
def mock_youtube_data_metadata(mocker):
    return mocker.patch("src.youtube_data.YouTubeData.metadata")


@pytest.fixture
def mock_youtube_data_metadata_with_return(mocker, mock_metadata):
    return mocker.patch(
        "src.youtube_data.YouTubeData.metadata", return_value=mock_metadata
    )


@pytest.fixture
def mock_get_output(mocker):
    return mocker.patch("src.cli.get_output", return_value="This is a test")


@pytest.fixture
def mock_get_transcript(mocker):
    return mocker.patch("src.cli.get_transcript", return_value="This is a test")


@pytest.fixture
def mock_slugify_video_title(mocker):
    return mocker.patch(
        "src.cli.slugify_video_title", return_value="this-is-a-test-video"
    )


@pytest.fixture
def mock_write_file(mocker):
    return mocker.patch("src.cli.write_file")


@pytest.fixture
def mock_youtube_data(mocker):
    return mocker.patch("src.youtube_data.YouTubeData")


class TestCli:
    def test_transcript_is_retrieved(
        self,
        runner,
        mock_transcript_get_transcript,
        mock_youtube_data__get_video,
        valid_url,
        mock_ai,
        mock_youtube_data_metadata_with_return,
    ):
        """Test that the transcript is retrieved from a valid YouTube URL."""
        with runner.isolated_filesystem():
            result = runner.invoke(
                app,
                [
                    "--no-takeaways",
                    "--no-summary",
                    "--no-metadata",
                    valid_url,
                ],
            )
            print(result.output)
            mock_youtube_data__get_video.assert_called_once()
            mock_transcript_get_transcript.assert_called_once()
            mock_ai.assert_not_called()
            assert result.exit_code == 0

    def test_summary_is_retrieved(
        self,
        runner,
        mock_transcript_get_transcript,
        mock_youtube_data__get_video,
        valid_url,
        mock_ai_summary,
        mock_youtube_metadata,
        mock_transcript_split,
    ):
        with runner.isolated_filesystem():
            result = runner.invoke(
                app,
                [
                    "--no-takeaways",
                    "--summary",
                    "--no-metadata",
                    valid_url,
                ],
            )
            mock_youtube_data__get_video.assert_called_once()
            mock_transcript_get_transcript.assert_called_once()
            mock_ai_summary.assert_called_once()
            assert result.exit_code == 0

    def test_takeaways_is_retrieved(
        self,
        runner,
        mock_transcript_get_transcript,
        mock_youtube_data__get_video,
        valid_url,
        mock_ai_takeaways,
        mock_youtube_metadata,
        mock_transcript_split,
    ):
        with runner.isolated_filesystem():
            result = runner.invoke(
                app,
                [
                    "--takeaways",
                    "--no-summary",
                    "--no-metadata",
                    valid_url,
                ],
            )
            mock_youtube_data__get_video.assert_called_once()
            mock_transcript_get_transcript.assert_called_once()
            mock_ai_takeaways.assert_called_once()
            assert result.exit_code == 0

    def test_metadata_is_retrieved(
        self,
        runner,
        mock_transcript_get_transcript,
        mock_youtube_data__get_video,
        valid_url,
        mock_youtube_data_metadata_with_return,
        mock_ai_takeaways,
        mock_ai_summary,
    ):
        with runner.isolated_filesystem():
            result = runner.invoke(
                app,
                [
                    "--no-takeaways",
                    "--no-summary",
                    "--metadata",
                    valid_url,
                ],
            )
            mock_youtube_data__get_video.assert_called_once()
            mock_transcript_get_transcript.assert_called_once()
            mock_ai_summary.assert_not_called()
            mock_ai_takeaways.assert_not_called()
            assert result.exit_code == 0

    def test_slugify_video_title(
        self,
        mock_youtube_data_metadata,
        mock_youtube_data__get_video,
        mock_metadata,
        runner,
    ):
        """Test slugify_video_title function."""
        with runner.isolated_filesystem():
            result = slugify_video_title(mock_metadata)

            assert result == "this-is-a-test-video"
            assert mock_metadata.title == "This is a Test Video"

    def test_write_flag_is_set(
        self,
        runner,
        mock_youtube_data_metadata_with_return,
        mock_youtube_data__get_video,
        valid_url,
        mock_get_transcript,
        mock_slugify_video_title,
        mock_write_file,
    ):
        with runner.isolated_filesystem():
            path = os.getcwd()
            result = runner.invoke(
                app,
                [
                    "--no-takeaways",
                    "--no-summary",
                    "--metadata",
                    "--write",
                    "--path",
                    path,
                    valid_url,
                ],
            )
            mock_write_file.assert_called_once()
            assert result.exit_code == 0

    def test_file_is_created(
        self,
        runner,
        mock_youtube_data_metadata_with_return,
        mock_youtube_data__get_video,
        valid_url,
        mock_get_transcript,
        mock_slugify_video_title,
        mock_write_file,
    ):
        with runner.isolated_filesystem():
            filename = "this-is-a-test-video"
            content = "This is a test video"
            path = os.getcwd()
            write_file(filename, content, path)

            assert os.path.isfile(os.path.join(path, f"{filename}.md"))
            with open(os.path.join(path, f"{filename}.md"), "r") as f:
                assert f.read() == content

    def test_write_file_raises_error_when_file_already_exists(
        self,
        runner,
        mock_youtube_data_metadata_with_return,
        mock_youtube_data__get_video,
        valid_url,
        mock_get_transcript,
        mock_slugify_video_title,
        mock_write_file,
    ):
        with runner.isolated_filesystem():
            filename = "this-is-a-test-video"
            content = "This is a test video"
            path = os.getcwd()
            write_file(filename, content, path)

            with pytest.raises(FileExistsError):
                write_file(filename, content, path)

    def test_get_youtube_data_raises_error_when_url_is_invalid(
        self,
        runner,
        mock_youtube_data_metadata_with_return,
        # mock_youtube_data__get_video,
        # valid_url,
        mock_get_transcript,
        mock_slugify_video_title,
        mock_write_file,
        mocker,
        mock_youtube_data,
    ):
        mocker.patch(
            "src.youtube_data.YouTubeData._get_video",
            side_effect=BadParameter("Invalid YouTube URL"),
        )

        # Call the function with an invalid YouTube URL
        with pytest.raises(SystemExit):
            get_youtube_data("invalid-url")

        # mocker.patch.object(YouTubeData, "_get_video", side_effect=Exception)
        # with runner.isolated_filesystem():
        #     with pytest.raises(Exception):
        #         get_youtube_data("invalid-url")
