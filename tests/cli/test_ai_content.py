import pytest
from hypothesis import given
from hypothesis import strategies as st
from langchain_core.messages import SystemMessage

import src.cli


def test_function_succeeds(mocker):
    mock_ai_openai_chat = mocker.patch("src.ai.openai_chat")
    mock_ai_openai_chat.return_value = (0, "bar")

    src.cli.get_ai_content(("foo", "bar"), "bar")

    mock_ai_openai_chat.assert_called_once_with(
        system_message=SystemMessage(content="bar"),
        temperature=1.0,
        transcript_chunks=("foo", "bar"),
    )


def test_function_fails(mocker):
    mock_ai_openai_chat = mocker.patch("src.ai.openai_chat")
    mock_ai_openai_chat.return_value = (1, "bar")

    with pytest.raises(ValueError):
        src.cli.get_ai_content(("foo", "bar"), "bar")

    mock_ai_openai_chat.assert_called_once_with(
        system_message=SystemMessage(content="bar"),
        temperature=1.0,
        transcript_chunks=("foo", "bar"),
    )
