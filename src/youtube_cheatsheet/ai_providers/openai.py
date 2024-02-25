import functools
import os

import langchain_openai
from langchain_core.messages import HumanMessage, SystemMessage
from returns.maybe import Maybe, Nothing, Some

import youtube_cheatsheet.exceptions


def chat_stream(
    system_message: SystemMessage,
    model: str = "gpt-3.5-turbo-0125",
    temperature: float = 0.0,
    transcript_chunks: tuple[str, ...] = (),
    index: int = 0,
    result: str = "",
) -> str:
    validate_inputs(system_message, model)
    if index == len(transcript_chunks):
        return result

    messages = [system_message, HumanMessage(content=transcript_chunks[index])]
    chat = langchain_openai.ChatOpenAI(temperature=temperature, model=model)

    return chat_stream(
        system_message,
        model,
        temperature,
        transcript_chunks,
        index + 1,
        result + "".join([chunk.content for chunk in chat.stream(messages)]),  # type: ignore
    )


def validate_inputs(system_message: SystemMessage, model: str) -> None:
    if model == "":
        raise youtube_cheatsheet.exceptions.InvalidModelError()
    if "OPENAI_API_KEY" not in os.environ:
        raise youtube_cheatsheet.exceptions.OpenAIKeyError()
    if system_message.content == "":
        raise youtube_cheatsheet.exceptions.InvalidSystemMessageError()


def get_takeaways(takeaways: bool, transcript_chunks: tuple[str, ...]) -> str | None:
    takeaways_message = SystemMessage(
        content="The user will provide a transcript. From the transcript, you will provide a bulleted list of key takeaways."
    )
    return (
        Maybe.from_optional(Some if takeaways else Nothing)
        .bind_optional(
            lambda _: ai_content(
                transcript_chunks=transcript_chunks, system_message=takeaways_message
            )
        )
        .value_or(None)
    )


def get_summary(summary: bool, transcript_chunks: tuple[str, ...]) -> str | None:
    summary_message = SystemMessage(
        content=(
            "The user will provide a transcript."
            "Reformat the transcript into an in-depth markdown blog post using sections and section headers."
            "The top level heading should be ###."
        )
    )
    return (
        Maybe.from_optional(Some if summary else Nothing)
        .bind_optional(
            lambda _: ai_content(
                transcript_chunks=transcript_chunks, system_message=summary_message
            )
        )
        .value_or(None)
    )


ai_content = functools.partial(chat_stream, temperature=1.0)
