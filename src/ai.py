import os
from typing import Tuple

import langchain_openai
from langchain_core.messages import HumanMessage, SystemMessage


def openai_chat(
    system_message: SystemMessage,
    model: str = "gpt-3.5-turbo-16k",
    temperature: float = 0.0,
    transcript_chunks: Tuple[str, ...] = (),
) -> tuple[int, str]:
    """Perform a chat conversation using the specified model and messages.

    Args:
        model (str): The model to use for the chat conversation.
            Defaults to "gpt-3.5-turbo-16k".
        temperature (float): The temperature parameter for generating
            responses. Defaults to 0.0.
        messages (list): The list of messages in the conversation.
            Must be specified.

    Returns:
        list: The list of generated responses.
    """
    validation_result, validation_value = validate_chat_inputs(system_message)
    if validation_result != 0:
        return (validation_result, validation_value)

    return (
        0,
        openai_chat_stream(system_message, model, temperature, transcript_chunks),
    )


def openai_chat_stream(
    system_message: SystemMessage,
    model: str = "gpt-3.5-turbo-16k",
    temperature: float = 0.0,
    transcript_chunks: Tuple[str, ...] = (),
    index: int = 0,
    result: str = "",
) -> str:
    if model == "":
        raise ValueError
    if index == len(transcript_chunks):
        return result

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


def validate_chat_inputs(system_message: SystemMessage) -> tuple[int, str]:
    if system_message is None:
        return (1, "system_message must be specified.")
    if system_message.content == "":
        return (2, "system_message.content must be specified.")
    if "OPENAI_API_KEY" not in os.environ:
        return (3, "OPENAI_API_KEY must be set in the environment.")
    return (0, "")
