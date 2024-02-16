#!/usr/bin/env python3
import functools
import pathlib
from sys import stderr
from typing import Optional, Tuple

import slugify
import typer
from jinja2 import Template
from langchain_core.messages import SystemMessage
from pytube import YouTube
from returns.maybe import Maybe, Nothing, Some
from returns.pipeline import flow
from returns.result import Failure, Result, Success
from typing_extensions import Annotated

import src.ai
import src.exceptions
import src.metadata
import src.transcript
import src.youtube_data

app: typer.Typer = typer.Typer(
    help="AI Assistant for YouTube videos", rich_markup_mode="rich"
)


@app.command()
def main(
    url: Annotated[str, typer.Argument(help="The URL of the YouTube video")],
    takeaways: Annotated[
        bool, typer.Option(help="Whether or not to include key takeaways")
    ] = True,
    summary: Annotated[
        bool, typer.Option(help="Whether or not to include an article summary")
    ] = True,
    metadata: Annotated[
        bool, typer.Option(help="Whether or not to include video metadata")
    ] = True,
    path: Annotated[
        Optional[pathlib.Path],
        typer.Option(help="The path to write the output file to"),
    ] = None,
) -> None:
    """
    Process YouTube videos and write the output to a file or stdout.

    :param url: The URL of the YouTube video
    :param takeaways: Whether or not to include key takeaways (default:
            True)
    :param summary: Whether or not to include an article summary (default:
            True)
    :param metadata: Whether or not to include video metadata (default:
            True)
    :param path: The path to write the output file to (default: None)
    """
    youtube_video = get_youtube_data_from_url(url)
    transcript = get_transcript(youtube_video)
    transcript_chunks = split_transcript(transcript)
    metadata_info = src.metadata.set_metadata(youtube_video)

    ai_content = functools.partial(
        src.ai.openai_chat_stream, temperature=1.0, transcript_chunks=transcript_chunks
    )
    takeaways_message = SystemMessage(
        content=(
            "The user will provide a transcript.From the transcript, you will provide a bulleted list of "
            f"key takeaways. At the top of the list, add a title: '## Key Takeaways — {metadata_info['title']}'"
        )
    )
    summary_message = SystemMessage(
        content=(
            "The user will provide a transcript. Reformat the transcript into an in-depth "
            "markdown blog post using sections and section headers."
            f"Add a section title: '## Summary — {metadata_info['title']}'"
        )
    )

    takeaway_content = (
        Maybe.from_optional(takeaways_message if takeaways else None)
        .bind_optional(lambda message: ai_content(system_message=message))
        .value_or(None)
    )
    summary_content = (
        Maybe.from_optional(summary_message if summary else None)
        .bind_optional(lambda message: ai_content(system_message=message))
        .value_or(None)
    )

    output = get_output(
        metadata_info["title"],
        metadata=src.metadata.metadata_string(metadata_info) if metadata else None,
        takeaways=takeaway_content if takeaways else None,
        summary=summary_content if summary else None,
    )

    write_file(metadata_info["title"], output, path) if path else print(output)


def get_output(
    title: str,
    metadata: str | None,
    takeaways: str | None,
    summary: str | None,
) -> str:
    """
    Assemble and return the formatted output string.

    :param title: The title of the output.
    :param metadata: The metadata related to the output. Can be None.
    :param takeaways: The takeaways from the output. Can be None.
    :param summary: The summary of the output. Can be None.


    """
    output_dict = {
        "title": title,
        "output_takeaways": takeaways,
        "output_summary": summary,
        "youtube_data_metadata": metadata,
    }
    template_str = (
        "# {{ title }}\n\n"
        "{% if output_summary %}{{ output_summary }}\n---\n{% endif %}"
        "{% if output_takeaways %}{{ output_takeaways }}\n---\n{% endif %}"
        "{% if youtube_data_metadata %}{{ youtube_data_metadata }}{% endif %}"
    )

    template = Template(template_str)
    output: str = template.render(**output_dict)
    return output


def write_file(title: str, content: str, path: pathlib.Path) -> None:
    """
    Write the output to a file.

    Args:
        title (str): The title of the file.
        content (str): The content to be written in the file.
        path (pathlib.Path): The path where the file will be created.

    Returns:
        None

    """
    file = flow(
        slugify.slugify(title),
        lambda filename: path.joinpath(filename).with_suffix(".md"),
    )

    result = Maybe.from_optional(validate_output_path(file, path)).unwrap()
    # print(result.unwrap())
    #     # .bind_optional(lambda _: file.write_text(content))
    #     .or_else_call(raise_exception(src.exceptions.OutputPathValidationError()))
    # )
    # print(validate_output_path(file, path))

    # if isinstance(result, Nothing):
    if result is Nothing:
        raise src.exceptions.OutputPathValidationError()

    file.write_text(content)


def validate_output_path(
    file_path: pathlib.Path, dir_path: pathlib.Path
) -> Maybe[bool]:
    """
    Validate the output path.

    :param file_path: pathlib.Path:
    :param dir_path: pathlib.Path:


    """
    conditions = not dir_path.exists() or not dir_path.is_dir() or file_path.exists()
    return Nothing if conditions else Some(True)
    # return Failure(None) if conditions else Success(True)


def get_youtube_data_from_url(url: str) -> YouTube:
    """
    Return YouTube data from given URL.

    :param url: str
    :param url: str:
    :param url: str:
    :returns: A YouTube object containing the data of the YouTube video.
    :raises ValueError: If the URL is invalid or the YouTube video data
    :raises cannot: be fetched

    """
    result, value = src.youtube_data.get_youtube_data_from_url(url)
    if result == 0:
        return value

    raise ValueError(value)


# def get_transcript(youtube_video: YouTube) -> str:
#     """
#     Retrieve the transcript for a given YouTube video.
#
#     Args:
#         youtube_video: A YouTube object representing the video for which to retrieve the transcript.
#
#     Returns:
#         str: The transcript of the YouTube video.
#
#     Raises:
#         src.exceptions.TranscriptGenerationFailedError: If the generation of the transcript fails.
#         NotImplementedError: If the result type is not handled.
#     """
#     result = src.transcript.get_transcript(youtube_video.video_id)
#
#     if isinstance(result, Success):
#         return result.unwrap()
#
#     if isinstance(result, Failure):
#         # Handle Failure case, possibly logging or raising an exception
#         # For demonstration, we'll just return a default value
#         print("No transcript found", file=stderr)
#         generate_result = src.transcript.generate_transcript(youtube_video)
#
#         if isinstance(generate_result, Success):
#             # If the result is a Success, extract and return the value
#             return result.unwrap()
#
#         if isinstance(generate_result, Failure):
#             # Handle Failure case, possibly logging or raising an exception
#             # For demonstration, we'll just return a default value
#             raise src.exceptions.TranscriptGenerationFailedError({result.failure()})
#
#     raise NotImplementedError(f"Unhandled result: {result}")


def get_transcript(youtube_video: YouTube) -> str:
    """Retrieve the transcript for a given YouTube video."""
    result = fetch_transcript(youtube_video)
    return handle_result(result, youtube_video)


def fetch_transcript(youtube_video: YouTube) -> Result:
    """Fetches the transcript and returns the result."""
    return src.transcript.get_transcript(youtube_video.video_id)


def handle_result(result: Result, youtube_video: YouTube) -> str:
    """Processes the result of a transcript fetch."""
    if not isinstance(result, (Success, Failure)):
        raise NotImplementedError(f"Unhandled result: {result}")

    if isinstance(result, Failure):
        print("No transcript found", file=stderr)
        return handle_transcript_generation(youtube_video, result)
    return result.unwrap()


def handle_transcript_generation(youtube_video: YouTube, result: Result) -> str:
    """Handles transcript generation in case of a fetch failure."""
    generate_result = src.transcript.generate_transcript(youtube_video)
    if isinstance(generate_result, Failure):
        raise src.exceptions.TranscriptGenerationFailedError(result.failure())
    return generate_result.unwrap()


def split_transcript(transcript: str) -> Tuple[str, ...]:
    """
    Split a transcript into multiple parts.

    :param transcript: str:
    :type transcript: str
    :param transcript: str:
    :param transcript: str:
    :returns: A tuple containing the split parts of the
    :rtype: Tuple[str, ...]
    :raises ValueError: If the split operation fails.

    Example:
    >>> transcript = "This is a transcript"
        >>> split_transcript(transcript)
        ("This is a transcript",)
    """
    result, value = src.transcript.split(transcript)
    if result == 1:
        raise ValueError(value)

    return value


if __name__ == "__main__":
    ...
