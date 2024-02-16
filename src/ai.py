import os
from typing import Tuple

import langchain_openai
from langchain_core.messages import HumanMessage, SystemMessage
from returns.result import Failure, Result, Success

import src.exceptions


def openai_chat_stream(
    system_message: SystemMessage,
    model: str = "gpt-3.5-turbo-1106",
    temperature: float = 0.0,
    transcript_chunks: Tuple[str, ...] = (),
    index: int = 0,
    result: str = "",
) -> str | None:
    """
    Perform a chat operation using the OpenAI language model.

    Args:
    ----
        system_message: A SystemMessage object representing the message from the system.
        model: A string specifying the model to be used for chat generation. Defaults to "gpt-3.5-turbo-16k".
        temperature: A float specifying the randomness of the generated responses. Defaults to 0.0.
        transcript_chunks: A tuple of strings representing the previous chat conversation transcript.
            Defaults to an empty tuple.
        index: An integer representing the index of the current chunk in the transcript_chunks. Defaults to 0.
        result: A string representing the accumulated chat result. Defaults to an empty string.

    Returns:
    -------
        A string representing the complete chat result after generating responses from the conversation transcript.

    Raises:
    ------
        ValueError: If the model parameter is an empty string.

    :param system_message: SystemMessage:
    :param model: str:  (Default value = "gpt-3.5-turbo-16k")
    :param temperature: float:  (Default value = 0.0)
    :param transcript_chunks: Tuple[str:
    :param ...]:  (Default value = ())
    :param index: int:  (Default value = 0)
    :param result: str:  (Default value = "")


    """
    if model == "":
        raise src.exceptions.InvalidModelError()
    if index == len(transcript_chunks):
        return result

    if isinstance(validate_chat_inputs(system_message), Failure):
        return None  # @TODO: change this to return a failure instead of returning None

    messages = [system_message, HumanMessage(content=transcript_chunks[index])]
    chat = langchain_openai.ChatOpenAI(temperature=temperature, model=model)

    return openai_chat_stream(
        system_message,
        model,
        temperature,
        transcript_chunks,
        index + 1,
        result + "".join([chunk.content for chunk in chat.stream(messages)]),  # type: ignore
    )


def validate_chat_inputs(system_message: SystemMessage) -> Result[bool, None]:
    """
    Validate the inputs for the chat operation.

    Args:
    ----
        system_message: A SystemMessage object that represents the system message to be validated.

    Returns:
    -------
        A tuple containing an integer status code and a string error message.

    Raises:
    ------
        None

    :param system_message: SystemMessage:


    """
    conditions = "OPENAI_API_KEY" not in os.environ or system_message.content == ""
    return Failure(None) if conditions else Success(True)
    # if any(system_message.content == "", "OPENAI_API_KEY" not in os.environ):

    # return 1, "system_message.content and OPENAI_API_KEY must be specified."
    # if system_message.content == "":
    #     return Failure(None)
    #     # return 2, "system_message.content must be specified."
    # if "OPENAI_API_KEY" not in os.environ:
    #     return Failure(None)
    #     # return 3, "OPENAI_API_KEY must be set in the environment."
    # # return 0, ""
    # return Success(True)
