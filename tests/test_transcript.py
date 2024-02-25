from datetime import datetime

import pytest
import pytube
import youtube_cheatsheet.exceptions
import youtube_transcript_api
from returns.result import Failure, Result, Success
from youtube_cheatsheet.transcript import (
    get_transcript,
    handle_result,
    split,
)


def mock_valid_video_object(mocker):
    mock_video = mocker.Mock(spec=pytube.YouTube)
    mock_video.title = "Test Title"
    mock_video.publish_date = datetime(2022, 1, 1)
    mock_video.author = "Test Author"
    mock_video.watch_url = "https://www.youtube.com/watch?v=12345"
    mock_video.description = "Test Description"
    mock_video.video_id = "12345"

    return mock_video


@pytest.fixture()
def mock_transcript_api(mocker):
    return mocker.patch("youtube_transcript_api.YouTubeTranscriptApi")


class TestGetTranscript:
    def test_success(self, mock_transcript_api):
        mock_transcript_api.get_transcript.return_value = [
            {"text": "bar"},
            {"text": "baz"},
        ]

        value = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")

        assert value.unwrap() == "bar baz"

    def test_not_found(self, mock_transcript_api) -> None:
        mock_transcript_api.get_transcript.side_effect = (
            youtube_transcript_api._errors.NoTranscriptFound("foo", ["en"], "bar baz")
        )
        mock_transcript_api.get_transcript.return_value = [
            {"text": "bar"},
            {"text": "baz"},
        ]

        result = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")
        assert result == Failure(None)
        # Returns the transcript if the result is a Success.

    def test_returns_transcript_if_success(self, mocker):
        # Mock the generate_transcript function to return a Success result
        mocker.patch(
            "youtube_cheatsheet.ai_providers.assemblyai.generate_transcript",
            return_value=Success("Transcript"),
        )

        # Create a mock YouTube object
        youtube_video = mocker.Mock(spec=pytube.YouTube)

        # Create a Success result
        result = Success("Transcript")

        # Call the handle_result function
        transcript = handle_result(result, youtube_video)

        # Assert that the transcript is returned
        assert transcript == "Transcript"

        # Raises a NotImplementedError if the result is not a Success or Failure.

    def test_raises_not_implemented_error_if_result_not_success_or_failure(
        self, mocker
    ):
        # Create a mock YouTube object
        youtube_video = mocker.Mock(spec=pytube.YouTube)

        # Create a mock Result object that is not a Success or Failure
        result = mocker.Mock(spec=Result)

        # Call the handle_result function and assert that it raises a NotImplementedError
        with pytest.raises(NotImplementedError):
            handle_result(result, youtube_video)

    def test_handle_result_failure(self, mocker):
        # Mock the handle_transcript_generation function to return a transcript
        generate_transcript = mocker.patch(
            "youtube_cheatsheet.transcript.handle_transcript_generation",
            return_value="Transcript",
        )

        # Create a mock YouTube object
        youtube_video = mocker.Mock(spec=pytube.YouTube)

        # Create a Failure result
        result = Failure(None)

        # Call the handle_result function
        handle_result(result, youtube_video)

        generate_transcript.assert_called_once()

    def test_handle_transcript_generation_failure(self, mocker, mock_youtube_data):
        mock_youtube_data.get_from_url.return_value = "YouTube Data"
        mock_generate_transcript = mocker.patch(
            "youtube_cheatsheet.ai_providers.assemblyai.generate_transcript"
        )
        mock_generate_transcript.return_value = Failure("Transcript")

        with pytest.raises(
            youtube_cheatsheet.exceptions.TranscriptGenerationFailedError
        ):
            youtube_cheatsheet.transcript.handle_transcript_generation(
                mock_youtube_data, Failure("Transcript")
            )

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

        with pytest.raises(youtube_cheatsheet.exceptions.TranscriptSplitError):
            youtube_cheatsheet.transcript.split_transcript("")

    def test_function_succeeds_with_two_chunks(self, mocker):
        mock_transcript_split = mocker.patch("youtube_cheatsheet.transcript.split")
        mock_transcript_split.return_value = (0, ("foo", "bar"))

        assert youtube_cheatsheet.transcript.split_transcript("") == ("foo", "bar")

    def test_function_succeeds_with_one_chunk(self, mocker):
        mock_transcript_split = mocker.patch("youtube_cheatsheet.transcript.split")
        mock_transcript_split.return_value = (0, ("foo",))

        assert youtube_cheatsheet.transcript.split_transcript("") == ("foo",)


class TestSplit:
    @pytest.mark.parametrize(
        ("split_test_return_value", "input", "expected_result", "expected_value"),
        [
            pytest.param(
                ["foo bar"], "foo bar", 0, ("foo bar",), id="succeeds_with_one_chunk"
            ),
            pytest.param(
                ["foo", "bar"],
                "foo bar",
                0,
                ("foo", "bar"),
                id="succeeds_with_multiple_chunks",
            ),
            pytest.param(
                [],
                "",
                1,
                ("The transcript must be specified.",),
                id="fails_with_empty_input",
            ),
        ],
    )
    def test_function(
        self, mocker, split_test_return_value, input, expected_result, expected_value
    ):
        mock_char_split = mocker.patch(
            "langchain.text_splitter.CharacterTextSplitter.from_tiktoken_encoder"
        )
        mock_char_split.return_value.split_text.return_value = split_test_return_value
        result, value = split(input)
        assert result == expected_result
        assert value == expected_value
