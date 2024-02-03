import os

import pytest
from langchain_core.messages import SystemMessage

from src.ai import openai_chat, openai_chat_stream, validate_chat_inputs


class TestAI:
    def test_openai_chat_success(self, mocker):
        mock_validation = mocker.patch("src.ai.validate_chat_inputs")
        mock_validation.return_value = (0, "")
        mock_stream = mocker.patch("src.ai.openai_chat_stream")

        openai_chat(
            SystemMessage(content="foo"),
            model="bar",
            temperature=0.5,
            transcript_chunks=("baz", "qux"),
        )

        assert mock_stream.call_count == 1

    def test_openai_chat_validation_error(self, mocker):
        mock_validation = mocker.patch("src.ai.validate_chat_inputs")
        mock_validation.return_value = (1, "foo")

        result, value = openai_chat(
            SystemMessage(content="foo"),
            model="bar",
            temperature=0.5,
            transcript_chunks=("baz", "qux"),
        )

        assert result == 1
        assert value == "foo"

    def test_openai_chat_stream_success(self, mocker):
        mock_chat_open_ai = mocker.patch("langchain_openai.ChatOpenAI")
        transcript_chunks = ("baz", "qux")

        openai_chat_stream(
            SystemMessage(content="foo"),
            model="gpt-3.5-turbo-16k",
            temperature=0.0,
            transcript_chunks=transcript_chunks,
            index=0,
            result="",
        )

        assert mock_chat_open_ai.call_count == len(transcript_chunks)
        assert mock_chat_open_ai.return_value.stream.call_count == len(
            transcript_chunks
        )

    def test_openai_chat_stream_model_empty(self):
        with pytest.raises(ValueError):
            openai_chat_stream(
                SystemMessage(content="foo"),
                model="",
                temperature=0.0,
                transcript_chunks=("baz", "qux"),
                index=0,
                result="",
            )

    @pytest.mark.parametrize(
        "system_message_content,environment_variables,expected_result,expected_value",
        [
            pytest.param(
                SystemMessage(content="foo"),
                {"OPENAI_API_KEY": "foo"},
                0,
                "",
                id="success",
            ),
            pytest.param(
                None,
                {"OPENAI_API_KEY": "foo"},
                1,
                "system_message must be specified.",
                id="system_message_none",
            ),
            pytest.param(
                SystemMessage(content=""),
                {"OPENAI_API_KEY": "foo"},
                2,
                "system_message.content must be specified.",
                id="system_message_content_empty",
            ),
            pytest.param(
                SystemMessage(content="foo"),
                {},
                3,
                "OPENAI_API_KEY must be set in the environment.",
                id="openai_api_key_not_exists",
            ),
        ],
    )
    def test_validate_chat_inputs(
        self,
        mocker,
        system_message_content,
        environment_variables,
        expected_result,
        expected_value,
    ):
        backup_key = (
            os.environ.pop("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else None
        )
        mocker.patch.dict(os.environ, environment_variables)
        result, value = validate_chat_inputs(system_message_content)
        assert result == expected_result
        assert value == expected_value
        if backup_key:
            os.environ["OPENAI_API_KEY"] = backup_key
