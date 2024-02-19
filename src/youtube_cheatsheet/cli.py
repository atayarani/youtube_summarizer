import functools
import pathlib
from sys import stderr
from typing import Annotated, Optional

import slugify
import typer
from jinja2 import Environment, FileSystemLoader, Template
from langchain_core.messages import SystemMessage
from pytube import YouTube
from returns.maybe import Maybe
from returns.result import Failure, Result, Success

import youtube_cheatsheet.ai
import youtube_cheatsheet.exceptions
import youtube_cheatsheet.metadata
import youtube_cheatsheet.transcript
import youtube_cheatsheet.youtube_data

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
    :param takeaways: Whether to include key takeaways (default: True)
    :param summary: Whether to include an article summary (default: True)
    :param metadata: Whether to include video metadata (default: True)
    :param path: The path to write the output file to (default: None)
    """
    youtube_video = get_youtube_data_from_url(url)
    transcript = get_transcript(youtube_video)
    transcript_chunks = split_transcript(transcript)
    metadata_info = youtube_cheatsheet.metadata.set_metadata(youtube_video)

    ai_content = functools.partial(
        youtube_cheatsheet.ai.openai_chat_stream,
        temperature=1.0,
        transcript_chunks=transcript_chunks,
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
        youtube_data_metadata=(
            youtube_cheatsheet.metadata.metadata_string(metadata_info)
            if metadata
            else None
        ),
        output_takeaways=takeaway_content if takeaway_content else None,
        output_summary=summary_content if summary else None,
    )

    write_file(metadata_info["title"], output, path) if path else print(output)


def setup_jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(
            pathlib.Path(__file__).parents[2].joinpath("templates")
        ),
        autoescape=True,
    )


def get_template(env: Environment, template_name: str = "output.md.j2") -> Template:
    return env.get_template(template_name)


def get_output(
    title: str,
    youtube_data_metadata: str | None = None,
    output_takeaways: str | None = None,
    output_summary: str | None = None,
) -> str:
    output_dict = locals()
    env = setup_jinja_env()
    template = get_template(env)
    return template.render(**output_dict)


def create_file_path(filename: str, path: pathlib.Path) -> pathlib.Path:
    # Separate the file creation process for better readability
    return path.joinpath(filename).with_suffix(".md")


def write_file(title: str, content: str, path: pathlib.Path) -> None:
    file = create_file_path(slugify.slugify(title), path)

    result = validate_output_path(file, path)
    if not result:
        raise youtube_cheatsheet.exceptions.OutputPathValidationError()

    file.write_text(content)


def validate_output_path(file_path: pathlib.Path, dir_path: pathlib.Path) -> bool:
    return dir_path.exists() and dir_path.is_dir() and not file_path.exists()


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
    result, value = youtube_cheatsheet.youtube_data.get_youtube_data_from_url(url)
    if result == 0:
        return value

    raise ValueError(value)


def get_transcript(youtube_video: YouTube) -> str:
    """Retrieve the transcript for a given YouTube video."""
    result = fetch_transcript(youtube_video)
    return handle_result(result, youtube_video)


def fetch_transcript(youtube_video: YouTube) -> Result:
    """Fetches the transcript and returns the result."""
    return youtube_cheatsheet.transcript.get_transcript(youtube_video.video_id)


def handle_result(result: Result, youtube_video: YouTube) -> str:
    """Processes the result of a transcript fetch."""
    if not isinstance(result, Success | Failure):
        raise NotImplementedError(f"Unhandled result: {result}")

    if isinstance(result, Failure):
        print("No transcript found", file=stderr)
        return handle_transcript_generation(youtube_video, result)
    return result.unwrap()


def handle_transcript_generation(youtube_video: YouTube, result: Result) -> str:
    """Handles transcript generation in case of a fetch failure."""
    generate_result = youtube_cheatsheet.transcript.generate_transcript(youtube_video)
    if isinstance(generate_result, Failure):
        raise youtube_cheatsheet.exceptions.TranscriptGenerationFailedError(
            result.failure()
        )
    return generate_result.unwrap()


def split_transcript(transcript: str) -> tuple[str, ...]:
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
    result, value = youtube_cheatsheet.transcript.split(transcript)
    if result == 1:
        raise ValueError(value)

    return value


if __name__ == "__main__":
    ...
