import pytest
import youtube_cheatsheet.video_providers.youtube.data
from langchain.docstore.document import Document
from returns.result import Failure, Success
from youtube_cheatsheet.ai_providers.assemblyai import generate_transcript


@pytest.fixture()
def mock_fetch(mocker):
    return mocker.patch(
        "youtube_cheatsheet.video_providers.youtube.audio.fetch_youtube_audio",
        return_value="audio_file_path",
    )


class TestGenerateTranscript:
    """Class to test the generate_transcript function."""

    # Generates a transcript for a YouTube video with valid URL.
    def test_generate_transcript_valid_url(self, mocker, mock_fetch):
        """
        Test the `generate_transcript` method with a valid URL.

        Args:
            mocker: The `mocker` object from the `pytest` framework.

        """
        # Mock fetch_youtube_audio function

        # Mock parse_youtube_audio function
        mock_parse = mocker.patch(
            "youtube_cheatsheet.ai_providers.assemblyai.parse_youtube_audio",
            return_value=[Document(page_content="Transcript content")],
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result = generate_transcript(youtube_mock)

        # Assert that the fetch_youtube_audio function was called with the correct arguments
        mock_fetch.assert_called_once_with(youtube_mock, mocker.ANY)

        # Assert that the parse_youtube_audio function was called with the correct arguments
        mock_parse.assert_called_once_with("audio_file_path")

        # Assert that the result is equal to the transcript content
        assert result == Success("Transcript content")

    # Returns the content of the transcript as a string.
    def test_generate_transcript_content_string(self, mocker, mock_fetch):
        """
        Test the generate_transcript_content_string method.

        Args:
            mocker: The mocker object used for mocking functions.

        Returns:
            None. This method does not return anything.
        """
        # Mock fetch_youtube_audio function

        # Mock parse_youtube_audio function
        mocker.patch(
            "youtube_cheatsheet.ai_providers.assemblyai.parse_youtube_audio",
            return_value=[Document(page_content="Transcript content")],
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result = generate_transcript(youtube_mock)

        assert result == Success("Transcript content")

    # Handles audio file download and parsing of the transcript.
    def test_generate_transcript_audio_download_and_parsing(self, mocker, mock_fetch):
        """
        Test generation of the transcript with audio file download and parsing.

        Args:
            mocker: The mocker object used for patching the functions.

        Returns:
            None

        Example Usage:

            mocker = ... # Create a mocker object

            test_generate_transcript_audio_download_and_parsing(self, mocker)
        """
        # Mock fetch_youtube_audio function

        # Mock parse_youtube_audio function
        mock_parse = mocker.patch(
            "youtube_cheatsheet.ai_providers.assemblyai.parse_youtube_audio",
            return_value=[Document(page_content="Transcript content")],
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result = generate_transcript(youtube_mock)

        # Assert that the fetch_youtube_audio function was called with the correct arguments
        mock_fetch.assert_called_once_with(youtube_mock, mocker.ANY)

        # Assert that the parse_youtube_audio function was called with the correct arguments
        mock_parse.assert_called_once_with("audio_file_path")

        # Assert that the result is equal to the transcript content
        assert result == Success("Transcript content")

    # Returns an empty string if transcript is empty.
    def test_generate_transcript_empty_transcript(self, mocker, mock_fetch):
        # Mock fetch_youtube_audio function

        # Mock parse_youtube_audio function
        mock_parse = mocker.patch(
            "youtube_cheatsheet.ai_providers.assemblyai.parse_youtube_audio",
            return_value=[],
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result = generate_transcript(youtube_mock)

        # Assert that the fetch_youtube_audio function was called with the correct arguments
        mock_fetch.assert_called_once_with(youtube_mock, mocker.ANY)
        mock_parse.assert_called_once_with("audio_file_path")

        # Assert that the result is an empty string
        assert result == Failure(None)

    def test_handle_transcript_generation_success(self, mocker):
        mock_youtube_data = mocker.Mock(
            spec=youtube_cheatsheet.video_providers.youtube.data.YouTubeData()
        )
        mock_youtube_data.get_from_url.return_value = "YouTube Data"
        mock_generate_transcript = mocker.patch(
            "youtube_cheatsheet.ai_providers.assemblyai.generate_transcript"
        )
        mock_generate_transcript.return_value = Success("Transcript")
        youtube_cheatsheet.transcript.handle_transcript_generation(
            mock_youtube_data, Success("Transcript")
        )
