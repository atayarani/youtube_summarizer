import os
from collections import namedtuple

# from langchain_openai import ChatOpenAI
import langchain_openai
import openai
import pytest
from langchain_core.messages import AIMessageChunk, HumanMessage, SystemMessage

from src.ai import AI
from src.metadata import Metadata


@pytest.fixture
def mock_youtube_data(mocker):
    return mocker.patch("src.youtube_data.YouTubeData")


@pytest.fixture
def valid_metadata():
    return Metadata(
        title="Title",
        publish_date="2022-01-01",
        author="Author",
        url="www.example.com",
        description="Description",
        video_id="12345",
    )


@pytest.fixture
def mock_ai__chat(mocker):
    return mocker.patch("src.ai.AI._chat")


@pytest.fixture
def mock_transcript(mocker):
    return mocker.patch("src.transcript.Transcript").return_value("transcript content")


@pytest.fixture
def mock_transcript_split(mocker):
    return mocker.patch("src.transcript.Transcript.split").return_value(
        ["chunk 1", "chunk 2"]
    )


@pytest.fixture
def mock_transcript_get_transcript(mocker):
    return mocker.patch("src.transcript.Transcript.get_transcript").return_value(
        "chunk 1 chunk 2"
    )


@pytest.fixture
def mock_youtube_data_metadata(mocker, valid_metadata):
    return mocker.patch("src.youtube_data.YouTubeData.metadata").return_value(
        valid_metadata
    )


@pytest.fixture
def mock_chat_openai(mocker):
    return mocker.patch("langchain_openai.ChatOpenAI")


class TestAi:
    def test_takeaways_call__chat(
        self, valid_metadata, mock_transcript, mock_youtube_data_metadata, mock_ai__chat
    ):
        ai = AI(mock_transcript, mock_youtube_data_metadata)
        ai.takeaways()
        mock_ai__chat.assert_called_once()

    def test_summary_call__chat(
        self, valid_metadata, mock_transcript, mock_youtube_data_metadata, mock_ai__chat
    ):
        ai = AI(mock_transcript, mock_youtube_data_metadata)
        ai.summary()
        mock_ai__chat.assert_called_once()

    def test__chat_returns_value_error_when_system_message_content_is_empty(
        self, mock_transcript, mock_youtube_data_metadata
    ):
        with pytest.raises(ValueError):
            ai = AI(mock_transcript, mock_youtube_data_metadata)
            ai._chat(system_message=SystemMessage(content=""), temperature=1.0)

    def test__chat_returns_value_error_when_system_message_content_is_none(
        self, mock_transcript, mock_youtube_data_metadata
    ):
        with pytest.raises(ValueError):
            ai = AI(mock_transcript, mock_youtube_data_metadata)
            ai._chat(system_message=SystemMessage(content=None), temperature=1.0)

    def test__chat_returns_value_error_when_system_message_is_none(
        self, mock_transcript, mock_youtube_data_metadata
    ):
        with pytest.raises(ValueError):
            ai = AI(mock_transcript, mock_youtube_data_metadata)
            ai._chat(system_message=None, temperature=1.0)

    def test__chat_returns_openai_key_error(
        self, mocker, mock_transcript, mock_youtube_data_metadata
    ):
        mocker.patch("src.ai.AI.check_openai_api_key").return_value = False
        with pytest.raises(AI.OpenAIKeyNotFoundError):
            ai = AI(mock_transcript, mock_youtube_data_metadata)
            ai._chat(system_message=SystemMessage(content="blah"), temperature=1.0)

    def test_check_openai_api_key_exists(
        self, mocker, mock_transcript, mock_youtube_data
    ):
        ai = AI(mock_transcript, mock_youtube_data)
        mocker.patch.dict(os.environ, {"OPENAI_API_KEY": "blah"})
        assert ai.check_openai_api_key()

    def test_check_openai_api_key_not_exists(self, mock_transcript, mock_youtube_data):
        ai = AI(mock_transcript, mock_youtube_data)
        os.environ.pop("OPENAI_API_KEY", None)
        assert not ai.check_openai_api_key()

    # @TODO: Add more test cases for _chat
    # I'm having a hard time figuring out the mock for ChatOpenAI
