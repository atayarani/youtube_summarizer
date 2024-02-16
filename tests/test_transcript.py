import pytest
import youtube_transcript_api
from langchain.docstore.document import Document
from returns.result import Failure, Success

from src.transcript import generate_transcript, get_transcript, split


class TestGetTranscript:
    """
    Class to test the success and failure scenarios of the `get_transcript` function.

    Methods:
    - test_success(mocker): Test the success scenario of the `get_transcript` function.
      - Parameters:
        - mocker: Mock object for patching `YouTubeTranscriptApi` class
      - Returns: None

    - test_not_found(mocker): Test the scenario where no transcript is found for a YouTube video in the `get_transcript` function.
      - Parameters:
        - mocker: Mock object for patching `YouTubeTranscriptApi` class
      - Returns: None
    """

    def test_success(self, mocker):
        """
        Test the success of the `get_transcript` method.

        Args:
            mocker: The mocker object from the pytest framework.

        """
        mock_transcript_api = mocker.patch(
            "youtube_transcript_api.YouTubeTranscriptApi"
        )
        mock_transcript_api.get_transcript.side_effect = None
        mock_transcript_api.get_transcript.return_value = [
            {"text": "bar"},
            {"text": "baz"},
        ]

        value = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")

        assert value == Success("bar baz")

    def test_not_found(self, mocker) -> None:
        """
        Test the behavior when no transcript is found for a given video.

        Args:
            mocker: The mocker object used for patching the "youtube_transcript_api.YouTubeTranscriptApi" module.

        Returns:
            None

        Example Usage:
            # Create mocker object
            mocker = MagicMock()

            # Create instance of the class containing the test_not_found method
            test_instance = TestClass()

            # Call the test_not_found method passing the mocker object
            test_instance.test_not_found(mocker)
        """
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

        result = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")
        assert result.failure()


class TestSplit:
    """
    Class representing the unit test for the `split` function.

    Methods:
    - `test_function`: Method for testing the `split` function.

    Attributes:
    - `split_test_return_value`: Expected return value from the `split_text` method of `mock_char_split`.
    - `input`: Test input for the `split` function.
    - `expected_result`: Expected result from the `split` function.
    - `expected_value`: Expected value from the `split` function.

    Example Usage:
    ```
    # Initialize the test class
    test_class = TestSplit()

    # Run the test_function method
    test_class.test_function(
        mocker, split_test_return_value, input, expected_result, expected_value
    )
    ```
    """

    @pytest.mark.parametrize(
        # "split_test_return_value,input,expected_result,expected_value",
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
        """
        Test the `split` function.

        Args:
            mocker: mocker object used for mocking
            split_test_return_value: list of strings representing the expected return value of mock_char_split.return_value.split_text
            input: string representing the input value for the test
            expected_result: expected result of the test
            expected_value: expected value of the test

        """
        mock_char_split = mocker.patch(
            "langchain.text_splitter.CharacterTextSplitter.from_tiktoken_encoder"
        )
        mock_char_split.return_value.split_text.return_value = split_test_return_value
        result, value = split(input)
        assert result == expected_result
        assert value == expected_value


class TestGenerateTranscript:
    """Class to test the generate_transcript function."""

    # Generates a transcript for a YouTube video with valid URL.
    def test_generate_transcript_valid_url(self, mocker):
        """
        Test the `generate_transcript` method with a valid URL.

        Args:
            mocker: The `mocker` object from the `pytest` framework.

        """
        # Mock fetch_youtube_audio function
        mock_fetch = mocker.patch(
            "src.transcript.fetch_youtube_audio", return_value="audio_file_path"
        )

        # Mock parse_youtube_audio function
        mock_parse = mocker.patch(
            "src.transcript.parse_youtube_audio",
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
    def test_generate_transcript_content_string(self, mocker):
        """
        Test the generate_transcript_content_string method.

        Args:
            mocker: The mocker object used for mocking functions.

        Returns:
            None. This method does not return anything.
        """
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
        result = generate_transcript(youtube_mock)

        assert result == Success("Transcript content")

    # Handles audio file download and parsing of the transcript.
    def test_generate_transcript_audio_download_and_parsing(self, mocker):
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
        mock_fetch = mocker.patch(
            "src.transcript.fetch_youtube_audio", return_value="audio_file_path"
        )

        # Mock parse_youtube_audio function
        mock_parse = mocker.patch(
            "src.transcript.parse_youtube_audio",
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
    def test_generate_transcript_empty_transcript(self, mocker):
        """
        Test case for the 'generate_transcript' method when the transcript is empty.

        Args:
            mocker: The mocker object from the pytest framework to create mocks and patches for testing.

        Test Steps:
        1. Mock the 'fetch_youtube_audio' function using the mocker object and set the return value to "audio_file_path".
        2. Mock the 'parse_youtube_audio' function using the mocker object and set the return value to an empty list.
        3. Create a mock YouTube object.
        4. Call the 'generate_transcript' function with the mocked YouTube object.
        5. Assert that the 'fetch_youtube_audio' function was called once with the correct arguments.
        6. Assert that the 'parse_youtube_audio' function was called once with the correct arguments.
        7. Assert that the result is equal to 1.
        8. Assert that the value is equal to "No transcript found".
        """
        # Mock fetch_youtube_audio function
        mock_fetch = mocker.patch(
            "src.transcript.fetch_youtube_audio", return_value="audio_file_path"
        )

        # Mock parse_youtube_audio function
        mock_parse = mocker.patch("src.transcript.parse_youtube_audio", return_value=[])

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function
        result = generate_transcript(youtube_mock)

        # Assert that the fetch_youtube_audio function was called with the correct arguments
        mock_fetch.assert_called_once_with(youtube_mock, mocker.ANY)
        mock_parse.assert_called_once_with("audio_file_path")

        # Assert that the result is an empty string
        assert result == Failure(None)

    # Raises an exception if YouTube video is not available.
    def test_generate_transcript_video_not_available(self, mocker):
        """
        Mock fetch_youtube_audio function to raise an exception.

        Args:
            mocker: The mocker object from the pytest library used for mocking the fetch_youtube_audio function.

        Raises:
            Exception: If the fetch_youtube_audio function raises an exception with the message "Video not available".

        Returns:
            None

        """
        mocker.patch(
            "src.transcript.fetch_youtube_audio",
            side_effect=Exception("Video not available"),
        )

        # Create a mock YouTube object
        youtube_mock = mocker.Mock()

        # Call the generate_transcript function and assert that it raises an exception
        with pytest.raises(Exception, match="Video not available"):
            generate_transcript(youtube_mock)
