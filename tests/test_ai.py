# import os

# import pytest
# import youtube_cheatsheet.exceptions
# from langchain_core.messages import SystemMessage
# from returns.result import Failure, Success
# from youtube_cheatsheet.ai import openai_chat_stream, validate_chat_inputs


# # class TestAI:
# # def test_openai_chat_stream_success(self, mocker):
# #     mock_chat_open_ai = mocker.patch("langchain_openai.ChatOpenAI")
# #     mock_validate_chat_inputs = mocker.patch(
# #         "youtube_cheatsheet.ai.validate_chat_inputs"
# #     )
# #     mock_validate_chat_inputs.return_value = Success(True)
# #     transcript_chunks = ("baz", "qux")

# #     openai_chat_stream(
# #         SystemMessage(content="foo"),
# #         model="gpt-3.5-turbo-16k",
# #         temperature=0.0,
# #         transcript_chunks=transcript_chunks,
# #         index=0,
# #         result="",
# #     )

# #     assert mock_chat_open_ai.call_count == len(transcript_chunks)
# #     assert mock_chat_open_ai.return_value.stream.call_count == len(
# #         transcript_chunks
# #     )

# # def test_openai_chat_stream_model_empty(self):
# #     with pytest.raises(youtube_cheatsheet.exceptions.InvalidModelError):
# #         openai_chat_stream(
# #             SystemMessage(content="foo"),
# #             model="",
# #             temperature=0.0,
# #             transcript_chunks=("baz", "qux"),
# #             index=0,
# #             result="",
# #         )

# # def test_openai_chat_stream_invalid_chat(self, mocker):
# #     mock_validate = mocker.patch("youtube_cheatsheet.ai.validate_chat_inputs")
# #     mock_validate.return_value = Failure(None)

# #     system_message = SystemMessage(content="Invalid message")
# #     transcript_chunks = ("Hello", "How are you")
# #     result = youtube_cheatsheet.ai.openai_chat_stream(
# #         system_message,
# #         model="gpt-3.5-turbo-16k",
# #         transcript_chunks=transcript_chunks,
# #     )

# #     assert result is None

# # @pytest.mark.parametrize(
# #     (
# #         "system_message_content",
# #         "environment_variables",
# #         "expected_result",
# #     ),
# #     [
# #         pytest.param(
# #             SystemMessage(content="foo"),
# #             {"OPENAI_API_KEY": "foo"},
# #             Success(True),
# #             id="success",
# #         ),
# #         pytest.param(
# #             SystemMessage(content=""),
# #             {"OPENAI_API_KEY": "foo"},
# #             Failure(None),
# #             id="system_message_content_empty",
# #         ),
# #         pytest.param(
# #             SystemMessage(content="foo"),
# #             {},
# #             Failure(None),
# #             id="openai_api_key_not_exists",
# #         ),
# #     ],
# # )
# # def test_validate_chat_inputs(
# #     self,
# #     mocker,
# #     system_message_content,
# #     environment_variables,
# #     expected_result,
# #     # expected_value,
# # ):
# #     """
# #     Test the validate_chat_inputs method.

# #     :param mocker:
# #     :param system_message_content:
# #     :param environment_variables:
# #     :param expected_result:

# #     """
# #     backup_key = (
# #         os.environ.pop("OPENAI_API_KEY") if "OPENAI_API_KEY" in os.environ else None
# #     )
# #     mocker.patch.dict(os.environ, environment_variables)
# #     result = validate_chat_inputs(system_message_content)
# #     assert result == expected_result
# #     # assert value == expected_value
# #     if backup_key:
# #         os.environ["OPENAI_API_KEY"] = backup_key
