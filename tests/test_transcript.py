
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


class TestSplit:
    @pytest.mark.parametrize(
        ("split_test_return_value", "input", "expected_value"),
        [
            pytest.param(
                ["foo bar"], "foo bar", ["foo bar"], id="succeeds_with_one_chunk"
            ),
            pytest.param(
                ["foo", "bar"],
                "foo bar",
                ["foo", "bar"],
                id="succeeds_with_multiple_chunks",
            ),
        ],
    )
    def test_function(self, mocker, split_test_return_value, input, expected_value):
        mock_char_split = mocker.patch(
            "langchain.text_splitter.CharacterTextSplitter.from_tiktoken_encoder"
        )
        mock_char_split.return_value.split_text.return_value = split_test_return_value
        assert split(input) == expected_value

    def test_function_returns_exception(self):
        assert isinstance(split(""), youtube_cheatsheet.exceptions.TranscriptSplitError)
