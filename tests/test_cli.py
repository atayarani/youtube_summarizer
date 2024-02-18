# import os

import pathlib

import pytest
import youtube_cheatsheet.exceptions
from returns.maybe import Nothing
from returns.result import Failure, Success
from typer.testing import CliRunner
from youtube_cheatsheet.cli import app, split_transcript, write_file


@pytest.fixture()
def runner():
    """
    Returns a CliRunner object.

    :returns: A CliRunner object that can be used to run command line interfaces in tests.

    :rtype: CliRunner

    """
    return CliRunner()


@pytest.fixture()
def url():
    """
    Returns the formatted URL.

    Args:
        url (str): The URL to be formatted.

    Returns:
        str: The formatted URL.

    Example:
        >>> url("https://www.youtube.com/watch?v=12345")
        'https://www.youtube.com/watch?v=12345'
    """
    return "https://www.youtube.com/watch?v=12345"


class TestSplitTranscript:
    """
    Test that the function successfully splits the transcript into one chunk.

    :param mocker: The mocker object for patching the transcript split function.
    """

    def test_function_succeeds_with_one_chunk(self, mocker):
        """
        Test that the function successfully splits the transcript into one chunk.

        Args:
            mocker: The mocker object used for patching the "youtube_cheatsheet.transcript.split" function.

        Returns:
            The output of the split_transcript function when an empty string is passed as input.

        Raises:
            AssertionError: If the split_transcript function does not return the expected output.
        """
        mock_transcript_split = mocker.patch("youtube_cheatsheet.transcript.split")
        mock_transcript_split.return_value = (0, ("foo",))

        assert split_transcript("") == ("foo",)

    def test_function_succeeds_with_two_chunks(self, mocker):
        """
        Test that the function successfully splits the transcript into two chunks.

        Args:
            mocker: The mocker object used for patching the "youtube_cheatsheet.transcript.split" function.

        Returns:
            The output of the split_transcript function when an empty string is passed as input.

        Raises:
            AssertionError: If the split_transcript function does not return the expected output.
        """
        mock_transcript_split = mocker.patch("youtube_cheatsheet.transcript.split")
        mock_transcript_split.return_value = (0, ("foo", "bar"))

        assert split_transcript("") == ("foo", "bar")

    def test_function_fails_with_zero_chunks(self, mocker):
        """
        Test that the function fails with zero chunks.

        Args:
            mocker: The mocker object from the pytest-mock library.

        Raises:
            ValueError: If the function fails to split the transcript into any chunks.
        """
        mock_transcript_split = mocker.patch("youtube_cheatsheet.transcript.split")
        mock_transcript_split.return_value = (1, ())

        with pytest.raises(ValueError):
            split_transcript("")


class TestWriteFile:
    """
    Test whether a function succeeds as expected by creating a temporary isolated filesystem using the provided test runner.

    :param runner: The test runner that will execute the test function.

    Example Usage:
    runner = TestRunner()
    self.test_function_succeeds(runner)
    """

    def test_function_succeeds(self, runner):
        """
        Test whether the function succeeds when given a runner.

        Args:
            runner: The runner object to use for testing.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        with runner.isolated_filesystem():
            write_file("foo", "bar", pathlib.Path())
            file = pathlib.Path("foo.md")
            assert file.exists()
            assert file.read_text() == "bar"

    def test_function_fails(self, mocker, runner):
        with runner.isolated_filesystem():
            mock_validate_output_path = mocker.patch(
                "youtube_cheatsheet.cli.validate_output_path"
            )
            # file = pathlib.Path("foo.md")
            mock_validate_output_path.return_value = Nothing
            with pytest.raises(youtube_cheatsheet.exceptions.OutputPathValidationError):
                write_file("foo", "bar", pathlib.Path("/home"))
            # file = pathlib.Path("foo.md")
            # assert not file.exists()


class TestMain:
    """
    Test if the YouTube video object is created successfully.

    Args:
        mocker: An instance of the mocker class.
        url: The URL of the YouTube video.
        runner: An instance of the runner class.

    Returns:
        None
    """

    def test_youtube_video_object_created(self, mocker, url, runner):
        """
        Test whether the YouTube video object is created when the YouTube URL is valid.

        Args:
            mocker: The mocker object used for patching the `get_youtube_data_from_url` method.
            url: The YouTube URL passed as a parameter to the test method.
            runner: The test runner object used for invoking the application.

        Raises:
            AssertionError: If the `result.exit_code` is not equal to 0.

        Returns:
            None
        """
        mock_get_youtube_data = mocker.patch(
            "youtube_cheatsheet.cli.get_youtube_data_from_url"
        )
        mocker.patch("youtube_cheatsheet.cli.get_transcript")
        mocker.patch("youtube_cheatsheet.cli.split_transcript")
        mocker.patch("youtube_cheatsheet.metadata.set_metadata")

        result = runner.invoke(
            app, ["--no-takeaways", "--no-summary", "--no-metadata", url]
        )

        mock_get_youtube_data.assert_called_once_with(url)
        assert result.exit_code == 0

    def test_youtube_video_object_not_created(self, mocker, url, runner):
        """
        Test whether the YouTube video object is not created when the YouTube URL is invalid.

        Args:
            mocker: The mocker object used for patching the `get_youtube_data_from_url` method.
            url: The YouTube URL passed as a parameter to the test method.
            runner: The test runner object used for invoking the application.

        Raises:
            AssertionError: If the `result.exit_code` is not equal to 1.

        Returns:
            None
        """
        mock_get_youtube_data = mocker.patch(
            "youtube_cheatsheet.cli.get_youtube_data_from_url"
        )
        mock_get_youtube_data.return_value = (1, "Invalid YouTube URL")

        result = runner.invoke(
            app, ["--no-takeaways", "--no-summary", "--no-metadata", url]
        )

        assert result.exit_code == 1

    def test_handle_transcript_generation_success(self, mocker):
        mock_get_youtube_data = mocker.patch(
            "youtube_cheatsheet.cli.get_youtube_data_from_url"
        )
        mock_get_youtube_data.return_value = "YouTube Data"
        mock_generate_transcript = mocker.patch(
            "youtube_cheatsheet.transcript.generate_transcript"
        )
        mock_generate_transcript.return_value = Success("Transcript")
        youtube_cheatsheet.cli.handle_transcript_generation(
            mock_get_youtube_data, Success("Transcript")
        )

    def test_handle_transcript_generation_failure(self, mocker):
        mock_get_youtube_data = mocker.patch(
            "youtube_cheatsheet.cli.get_youtube_data_from_url"
        )
        mock_get_youtube_data.return_value = "YouTube Data"
        mock_generate_transcript = mocker.patch(
            "youtube_cheatsheet.transcript.generate_transcript"
        )
        mock_generate_transcript.return_value = Failure("Transcript")

        with pytest.raises(
            youtube_cheatsheet.exceptions.TranscriptGenerationFailedError
        ):
            youtube_cheatsheet.cli.handle_transcript_generation(
                mock_get_youtube_data, Failure("Transcript")
            )

    # @pytest.mark.parametrize(
    #     "parameters",
    #     [
    #         pytest.param(["--takeaways", "--no-summary"], id="takeaways"),
    #         pytest.param(["--no-takeaways", "--summary"], id="summary"),
    #     ],
    # )
    # def test_fetch_ai_content(self, mocker, runner, url, parameters):
    #     """
    #     Test whether the fetch_ai_content function is called successfully.
    #
    #     Args:
    #         mocker: The mocker object used for mocking functions and classes in the test.
    #         runner: The runner object used for invoking the app in the test.
    #         url: The URL of the web page from where the AI content needs to be fetched.
    #         parameters: The list of parameters to be passed to the app in the test.
    #
    #     """
    #     mocker.patch("youtube_cheatsheet.cli.get_youtube_data_from_url")
    #     mocker.patch("youtube_cheatsheet.cli.get_transcript")
    #     mocker.patch("youtube_cheatsheet.cli.split_transcript")
    #     mocker.patch("youtube_cheatsheet.metadata.set_metadata")
    #     mock_ai_content = mocker.patch("youtube_cheatsheet.cli.get_ai_content")
    #
    #     result = runner.invoke(app, [*parameters, "--no-metadata", url])
    #
    #     mock_ai_content.assert_called_once()
    #     assert result.exit_code == 0

    # def test_write_output(self, mocker, runner, url):
    #     """
    #     Test whether the write_output function is called successfully.
    #
    #     Args:
    #         mocker: The mocker object used for patching functions in the test.
    #         runner: The runner object used for invoking the app in the test.
    #         url: The URL of the YouTube video being tested.
    #
    #     """
    #     mocker.patch("youtube_cheatsheet.cli.get_youtube_data_from_url")
    #     mocker.patch("youtube_cheatsheet.cli.get_transcript")
    #     mocker.patch("youtube_cheatsheet.cli.split_transcript")
    #     mocker.patch("youtube_cheatsheet.metadata.set_metadata")
    #     mock_slugify = mocker.patch("youtube_cheatsheet.cli.slugify_video_title")
    #     mock_write_file = mocker.patch("youtube_cheatsheet.cli.write_file")
    #
    #     with runner.isolated_filesystem():
    #         result = runner.invoke(
    #             app,
    #             ["--no-takeaways", "--no-summary", "--no-metadata", "--path", ".", url],
    #         )
    #
    #         mock_slugify.assert_called_once()
    #         mock_write_file.assert_called_once()
    #         assert result.exit_code == 0
