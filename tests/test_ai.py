# Generated by CodiumAI
import os

# Dependencies:
# pip install pytest-mock
import pytest
from langchain_core.messages import SystemMessage

from src.ai import AI


class MockTranscript:
    def __init__(self, content, metadata):
        self.content = content
        self.metadata = metadata


class MockMetadata:
    def __init__(self, title, publish_date, author, url):
        self.title = title
        self.publish_date = publish_date
        self.author = author
        self.url = url


class TestTakeaways:
    # Raises a ValueError when messages is None.
    def test_raises_value_error_when_messages_is_none(self, mocker):
        # Create an instance of the AI class
        ai = AI(
            MockTranscript(
                "This is a transcript",
                MockMetadata(
                    title="Test title",
                    publish_date="2021-01-01",
                    author="Test author",
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                ),
            )
        )

        # Call the takeaways method with messages set to None
        with pytest.raises(ValueError):
            ai._chat(temperature=0.0, messages=None)

    # Raises a KeyError when the OPENAI_API_KEY environment variable is not set.
    def test_raises_key_error_when_openai_api_key_not_set(self, mocker):
        # Create a mock Transcript object
        class MockTranscript:
            def __init__(self, content, metadata):
                self.content = content
                self.metadata = metadata

        key = os.environ.pop("OPENAI_API_KEY", None)
        # Create an instance of the AI class without setting OPENAI_API_KEY environment variable
        with pytest.raises(KeyError):
            ai = AI(MockTranscript("This is a transcript", {"title": "Test"}))

        os.environ["OPENAI_API_KEY"] = key

    # Handles edge cases when the transcript is too long.
    def test_handles_edge_cases_when_transcript_is_too_long(self, mocker):
        # Mock the ChatOpenAI class
        class MockChatOpenAI:
            def __init__(self, temperature, model):
                pass

            def stream(self, messages):
                return [
                    SystemMessage(content="Key takeaway 1"),
                    SystemMessage(content="Key takeaway 2"),
                ]

        mocker.patch("src.ai.ChatOpenAI", MockChatOpenAI)

        # Create an instance of the AI class
        ai = AI(
            MockTranscript(
                "This is a very long transcript" * 1000,
                MockMetadata(
                    title="Test title",
                    publish_date="2021-01-01",
                    author="Test author",
                    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                ),
            )
        )

        # Call the takeaways method
        result = ai.takeaways()

        # Assert that the result is a list
        assert isinstance(result, list)

        # Assert that the result contains the expected key takeaways
        assert result == ["Key takeaway 1", "Key takeaway 2"]
