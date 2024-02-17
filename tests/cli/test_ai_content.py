# import pytest
# from langchain_core.messages import SystemMessage
#
# import youtube_cheatsheet.cli
#
#
# def test_function_succeeds(mocker) -> None:
#     """
#     Test if the function 'youtube_cheatsheet.cli.get_ai_content' succeeds when called with specific parameters.
#
#     Args:
#         mocker: The mocker parameter is used to create a patch of the "youtube_cheatsheet.ai.openai_chat" method.
#
#     Returns:
#         None.
#     """
#     mock_ai_openai_chat = mocker.patch("youtube_cheatsheet.ai.openai_chat")
#     mock_ai_openai_chat.return_value = (0, "bar")
#
#     youtube_cheatsheet.cli.get_ai_content(("foo", "bar"), "bar")
#
#     mock_ai_openai_chat.assert_called_once_with(
#         system_message=SystemMessage(content="bar"),
#         temperature=1.0,
#         transcript_chunks=("foo", "bar"),
#     )
#
#
# def test_function_fails(mocker):
#     """
#     Test if the function `youtube_cheatsheet.cli.get_ai_content(("foo", "bar"), "bar")` raises a ValueError.
#
#     Args:
#         mocker: The mocker object that is used to create a mock patch.
#
#     Raises:
#         ValueError: If the function `youtube_cheatsheet.cli.get_ai_content(("foo", "bar"), "bar")` does not raise a ValueError.
#
#     Returns:
#         None
#     """
#     mock_ai_openai_chat = mocker.patch("youtube_cheatsheet.ai.openai_chat")
#     mock_ai_openai_chat.return_value = (1, "bar")
#
#     with pytest.raises(ValueError):
#         youtube_cheatsheet.cli.get_ai_content(("foo", "bar"), "bar")
#
#     mock_ai_openai_chat.assert_called_once_with(
#         system_message=SystemMessage(content="bar"),
#         temperature=1.0,
#         transcript_chunks=("foo", "bar"),
#     )
