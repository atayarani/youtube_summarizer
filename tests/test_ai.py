import os

import pytest
from langchain_core.messages import SystemMessage
from returns.result import Failure, Success

import src.exceptions
from src.ai import openai_chat_stream, validate_chat_inputs


class TestAI:
    """
    Test the openai_chat method when it successfully calls the openai_chat method.

    :param mocker: The mocker instance for pytest.

    """

    def test_openai_chat_stream_success(self, mocker):
        """
        Tests the success case of the `openai_chat_stream` method.

        Args:
            mocker: The `mocker` object used for patching the `ChatOpenAI` method.

        """
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
        """
        Test case for openai_chat_stream() when model parameter is empty.

        This test case verifies that when the model parameter is empty,
        a ValueError is raised. It uses pytest.raises() to assert that a
        ValueError exception is raised when the method is called with an
        empty model parameter.

        Parameters:
        - self: The instance of the test class.

        Return:
        - None

        Raises:
        - ValueError: If the model parameter is empty.

        Example:
        >>> test_openai_chat_stream_model_empty(self)
        """
        with pytest.raises(src.exceptions.InvalidModelError):
            openai_chat_stream(
                SystemMessage(content="foo"),
                model="",
                temperature=0.0,
                transcript_chunks=("baz", "qux"),
                index=0,
                result="",
            )

    def test_openai_chat_stream_invalid_chat(self, mocker):
        mock_validate = mocker.patch("src.ai.validate_chat_inputs")
        mock_validate.return_value = Failure(None)

        system_message = SystemMessage(content="Invalid message")
        transcript_chunks = ("Hello", "How are you")
        result = src.ai.openai_chat_stream(
            system_message,
            model="gpt-3.5-turbo-16k",
            transcript_chunks=transcript_chunks,
        )

        assert result is None

    @pytest.mark.parametrize(
        (
            "system_message_content",
            "environment_variables",
            "expected_result",
        ),
        [
            pytest.param(
                SystemMessage(content="foo"),
                {"OPENAI_API_KEY": "foo"},
                Success(True),
                id="success",
            ),
            pytest.param(
                SystemMessage(content=""),
                {"OPENAI_API_KEY": "foo"},
                Failure(None),
                id="system_message_content_empty",
            ),
            pytest.param(
                SystemMessage(content="foo"),
                {},
                Failure(None),
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
        # expected_value,
    ):
        """
        Test the validate_chat_inputs method.

        :param mocker:
        :param system_message_content:
        :param environment_variables:
        :param expected_result:

        """
        backup_key = (
            os.environ.pop("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else None
        )
        mocker.patch.dict(os.environ, environment_variables)
        result = validate_chat_inputs(system_message_content)
        assert result == expected_result
        # assert value == expected_value
        if backup_key:
            os.environ["OPENAI_API_KEY"] = backup_key
