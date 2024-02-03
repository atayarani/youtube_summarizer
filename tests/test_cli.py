# import os

import pathlib

import pytest
from hypothesis import given
from hypothesis import strategies as st
from typer.testing import CliRunner

import src.cli
from src.cli import (
    app,
    get_transcript,
    slugify_video_title,
    split_transcript,
    write_file,
)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def url():
    return "https://www.youtube.com/watch?v=12345"


class TestGetTranscript:
    def test_function_succeeds(self, mocker):
        mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
        mock_transcript_get_transcript.return_value = (0, "foo")
        mock_youtube_video = mocker.patch("pytube.YouTube")
        mock_youtube_video.video_id = "12345"

        assert get_transcript(mock_youtube_video) == "foo"

    def test_transcript_not_found(self, mocker):
        mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
        mock_transcript_get_transcript.return_value = (1, "foo")
        mock_youtube_video = mocker.patch("pytube.YouTube")
        mock_youtube_video.video_id = "12345"
        mock_transcript_generate_transcript = mocker.patch(
            "src.transcript.generate_transcript"
        )

        get_transcript(mock_youtube_video)

        mock_transcript_generate_transcript.assert_called_once_with(mock_youtube_video)

    def test_transcripts_disabled(self, mocker):
        mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
        mock_transcript_get_transcript.return_value = (2, "foo")
        mock_youtube_video = mocker.patch("pytube.YouTube")
        mock_youtube_video.video_id = "12345"
        mock_transcript_generate_transcript = mocker.patch(
            "src.transcript.generate_transcript"
        )

        get_transcript(mock_youtube_video)

        mock_transcript_generate_transcript.assert_called_once_with(mock_youtube_video)

    def test_not_implemented_error(self, mocker):
        mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
        mock_transcript_get_transcript.return_value = (99, "foo")
        mock_youtube_video = mocker.patch("pytube.YouTube")
        mock_youtube_video.video_id = "12345"

        with pytest.raises(NotImplementedError):
            get_transcript(mock_youtube_video)


class TestSplitTranscript:
    def test_function_succeeds_with_one_chunk(self, mocker):
        mock_transcript_split = mocker.patch("src.transcript.split")
        mock_transcript_split.return_value = (0, tuple(("foo",)))

        assert split_transcript("") == ("foo",)

    def test_function_succeeds_with_two_chunks(self, mocker):
        mock_transcript_split = mocker.patch("src.transcript.split")
        mock_transcript_split.return_value = (0, tuple(("foo", "bar")))

        assert split_transcript("") == ("foo", "bar")

    def test_function_fails_with_zero_chunks(self, mocker):
        mock_transcript_split = mocker.patch("src.transcript.split")
        mock_transcript_split.return_value = (1, tuple(()))

        with pytest.raises(ValueError):
            split_transcript("")


class TestSlugifyVideoTitle:
    def test_function_succeeds(self):
        assert slugify_video_title("This is a Test Video") == "this-is-a-test-video"

    @given(title=st.text())
    def test_idempotent_slugify_video_title(self, title: str) -> None:
        result = src.cli.slugify_video_title(title=title)
        repeat = src.cli.slugify_video_title(title=result)
        assert result == repeat, (result, repeat)

    @given(title=st.text())
    def test_fuzz_slugify_video_title(self, title: str) -> None:
        src.cli.slugify_video_title(title=title)


class TestWriteFile:
    def test_function_succeeds(self, mocker, runner):
        # mock_validate_output_path = mocker.patch("src.cli.validate_output_path")
        # mock_validate_output_path.return_value = (0, None)

        with runner.isolated_filesystem():
            write_file("foo", "bar", pathlib.Path("."))
            file = pathlib.Path("foo.md")
            assert file.exists()
            assert file.read_text() == "bar"

    def test_function_fails(self, mocker, runner):
        with runner.isolated_filesystem():
            with pytest.raises(FileExistsError):
                mock_validate_output_path = mocker.patch("src.cli.validate_output_path")
                file = pathlib.Path("foo.md")
                mock_validate_output_path.return_value = (
                    1,
                    FileExistsError(f"{file} already exists"),
                )
                write_file("foo", "bar", pathlib.Path("/home"))


class TestMain:
    def test_youtube_video_object_created(self, mocker, url, runner):
        mock_get_youtube_data = mocker.patch("src.cli.get_youtube_data_from_url")
        mocker.patch("src.cli.get_transcript")
        mocker.patch("src.cli.split_transcript")
        mocker.patch("src.metadata.set_metadata")

        result = runner.invoke(
            app, ["--no-takeaways", "--no-summary", "--no-metadata", url]
        )

        mock_get_youtube_data.assert_called_once_with(url)
        assert result.exit_code == 0

    def test_youtube_video_object_not_created(self, mocker, url, runner):
        mock_get_youtube_data = mocker.patch("src.cli.get_youtube_data_from_url")
        mock_get_youtube_data.return_value = (1, "Invalid YouTube URL")

        result = runner.invoke(
            app, ["--no-takeaways", "--no-summary", "--no-metadata", url]
        )

        assert result.exit_code == 1

    @pytest.mark.parametrize(
        "parameters",
        [
            pytest.param(["--takeaways", "--no-summary"], id="takeaways"),
            pytest.param(["--no-takeaways", "--summary"], id="summary"),
        ],
    )
    def test_fetch_ai_content(self, mocker, runner, url, parameters):
        mocker.patch("src.cli.get_youtube_data_from_url")
        mocker.patch("src.cli.get_transcript")
        mocker.patch("src.cli.split_transcript")
        mocker.patch("src.metadata.set_metadata")
        mock_ai_content = mocker.patch("src.cli.get_ai_content")

        result = runner.invoke(app, parameters + ["--no-metadata", url])

        mock_ai_content.assert_called_once()
        assert result.exit_code == 0

    def test_write_output(self, mocker, runner, url):
        mocker.patch("src.cli.get_youtube_data_from_url")
        mocker.patch("src.cli.get_transcript")
        mocker.patch("src.cli.split_transcript")
        mocker.patch("src.metadata.set_metadata")
        mock_slugify = mocker.patch("src.cli.slugify_video_title")
        mock_write_file = mocker.patch("src.cli.write_file")

        with runner.isolated_filesystem():
            result = runner.invoke(
                app, ["--no-takeaways", "--no-summary", "--no-metadata", "--write", url]
            )

            mock_slugify.assert_called_once()
            mock_write_file.assert_called_once()
            assert result.exit_code == 0
