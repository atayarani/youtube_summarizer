import pytest
import youtube_transcript_api
from langchain.docstore.document import Document

import src.transcript
from src.transcript import generate_transcript, get_transcript, split


class TestGetTranscript:
    def test_success(self, mocker):
        mock_transcript_api = mocker.patch(
            "youtube_transcript_api.YouTubeTranscriptApi"
        )
        mock_transcript_api.get_transcript.side_effect = None
        mock_transcript_api.get_transcript.return_value = [
            {"text": "bar"},
            {"text": "baz"},
        ]

        result, value = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")
        assert result == 0
        assert value == "bar baz"

    def test_not_found(self, mocker):
        mock_transcript_api = mocker.patch(
            "youtube_transcript_api.YouTubeTranscriptApi"
        )
        mock_transcript_api.get_transcript.side_effect = (
            youtube_transcript_api._errors.NoTranscriptFound("foo", ["en"], "bar baz")
        )
        mock_transcript_api.get_transcript.return_value = [
            {"text": "bar"},
            {"text": "baz"},
        ]

        result, value = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")
        assert result == 1


class TestSplit:
    @pytest.mark.parametrize(
        "split_test_return_value,input,expected_result,expected_value",
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


class TestGenerateTranscript:
    # Generates a transcript for a YouTube video with valid URL.
    def test_generate_transcript_valid_url(self, mocker):
        # Mock fetch_youtube_audio function
        mocker.patch(
            "src.transcript.fetch_youtube_audio", return_value="audio_file_path"
        )

        # Mock parse_youtube_audio function
        mocker.patch(
            "src.transcript.parse_youtube_audio",
            return_value=[Document(page_content="Transcript content")],
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result, value = generate_transcript(youtube_mock)

        # Assert that the fetch_youtube_audio function was called with the correct arguments
        src.transcript.fetch_youtube_audio.assert_called_once_with(
            youtube_mock, mocker.ANY
        )

        # Assert that the parse_youtube_audio function was called with the correct arguments
        src.transcript.parse_youtube_audio.assert_called_once_with("audio_file_path")

        # Assert that the result is equal to the transcript content
        assert result == 0
        assert value == "Transcript content"

    # Returns the content of the transcript as a string.
    def test_generate_transcript_content_string(self, mocker):
        # Mock fetch_youtube_audio function
        mocker.patch(
            "src.transcript.fetch_youtube_audio", return_value="audio_file_path"
        )

        # Mock parse_youtube_audio function
        mocker.patch(
            "src.transcript.parse_youtube_audio",
            return_value=[Document(page_content="Transcript content")],
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result, value = generate_transcript(youtube_mock)

        assert result == 0
        assert value == "Transcript content"

    # Handles audio file download and parsing of the transcript.
    def test_generate_transcript_audio_download_and_parsing(self, mocker):
        # Mock fetch_youtube_audio function
        mocker.patch(
            "src.transcript.fetch_youtube_audio", return_value="audio_file_path"
        )

        # Mock parse_youtube_audio function
        mocker.patch(
            "src.transcript.parse_youtube_audio",
            return_value=[Document(page_content="Transcript content")],
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result, value = generate_transcript(youtube_mock)

        # Assert that the fetch_youtube_audio function was called with the correct arguments
        src.transcript.fetch_youtube_audio.assert_called_once_with(
            youtube_mock, mocker.ANY
        )

        # Assert that the parse_youtube_audio function was called with the correct arguments
        src.transcript.parse_youtube_audio.assert_called_once_with("audio_file_path")

        # Assert that the result is equal to the transcript content
        assert result == 0
        assert value == "Transcript content"

    # Returns an empty string if transcript is empty.
    def test_generate_transcript_empty_transcript(self, mocker):
        # Mock fetch_youtube_audio function
        mocker.patch(
            "src.transcript.fetch_youtube_audio", return_value="audio_file_path"
        )

        # Mock parse_youtube_audio function
        mocker.patch("src.transcript.parse_youtube_audio", return_value=[])

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result, value = generate_transcript(youtube_mock)

        # Assert that the fetch_youtube_audio function was called with the correct arguments
        src.transcript.fetch_youtube_audio.assert_called_once_with(
            youtube_mock, mocker.ANY
        )

        # Assert that the parse_youtube_audio function was called with the correct arguments
        src.transcript.parse_youtube_audio.assert_called_once_with("audio_file_path")

        # Assert that the result is an empty string
        assert result == 1
        assert value == "No transcript found"

    # Raises an exception if YouTube video is not available.
    def test_generate_transcript_video_not_available(self, mocker):
        # Mock fetch_youtube_audio function to raise an exception
        mocker.patch(
            "src.transcript.fetch_youtube_audio",
            side_effect=Exception("Video not available"),
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function and assert that it raises an exception
        with pytest.raises(Exception, match="Video not available"):
            generate_transcript(youtube_mock)
