import os

import langchain_openai
from langchain_core.messages import HumanMessage, SystemMessage
from returns.result import Failure, Result, Success

import youtube_cheatsheet.exceptions


def openai_chat_stream(
    system_message: SystemMessage,
    model: str = "gpt-3.5-turbo-0125",
    temperature: float = 0.0,
    transcript_chunks: tuple[str, ...] = (),
    index: int = 0,
    result: str = "",
) -> str | None:
    if model == "":
        raise youtube_cheatsheet.exceptions.InvalidModelError()
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
    conditions = "OPENAI_API_KEY" not in os.environ or system_message.content == ""
    return Failure(None) if conditions else Success(True)
