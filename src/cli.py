#!/usr/bin/env python3
import pathlib
from sys import stderr
from typing import Optional, Tuple

import slugify
import typer
from jinja2 import Template
from langchain_core.messages import SystemMessage
from pytube import YouTube
from typing_extensions import Annotated

import src.ai
import src.exceptions
import src.metadata
import src.transcript
import src.youtube_data

app = typer.Typer(help="AI Assistant for YouTube videos", rich_markup_mode="rich")


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
    Main function to process YouTube video and generate summary.

    Args:
        url (str): The URL of the YouTube video.
        takeaways (bool): Flag indicating whether to generate takeaways from the video.
        summary (bool): Flag indicating whether to generate a summary.
        metadata (bool): Flag indicating whether to print video metadata.
        path (str): The path to write the output file.

    Returns:
        None
    """

    youtube_video = get_youtube_data_from_url(url)
    transcript = get_transcript(youtube_video)
    transcript_chunks = split_transcript(transcript)
    metadata_info = src.metadata.set_metadata(youtube_video)

    # if any([takeaways, summary]):
    if takeaways:
        takeaway_content = get_ai_content(
            transcript_chunks,
            system_message_content=(
                "The user will provide a transcript.From the transcript, you will provide a bulleted list of "
                f"key takeaways. At the top of the list, add a title: '## Key Takeaways — {metadata_info['title']}'"
            ),
        )
    if summary:
        summary_content = get_ai_content(
            transcript_chunks,
            system_message_content=(
                "The user will provide a transcript."
                "reformat the transcript  into an in-depth "
                "markdown blog post using sections and section headers."
                f"Add a section title: '## Summary — {metadata_info['title']}'"
            ),
        )

    output = get_output(
        metadata_info["title"],
        metadata=str(metadata_info) if metadata else None,
        takeaways=takeaway_content if takeaways else None,
        summary=summary_content if summary else None,
    )

    if path is not None:
        filename = slugify_video_title(metadata_info["title"])
        write_file(filename, output, path)
    else:
        print(output)


def get_output(
    title: str,
    metadata: str | None,
    takeaways: str | None,
    summary: str | None,
) -> str:
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
    return template.render(**output_dict)


def slugify_video_title(title: str) -> str:
    return slugify.slugify(title)


def write_file(filename: str, content: str, path: pathlib.Path) -> None:
    file = path.joinpath(filename).with_suffix(".md")
    result, value = validate_output_path(file, path)

    if value is not None:
        raise value

    file.write_text(content)


def validate_output_path(
    file_path: pathlib.Path, dir_path: pathlib.Path
) -> tuple[int, OSError | None]:
    if file_path.exists():
        return (1, FileExistsError(f"{file_path} already exists"))
    elif not dir_path.is_dir():
        return (2, NotADirectoryError(f"{dir_path} is not a directory"))
    elif not dir_path.exists():
        return (3, FileNotFoundError(f"{dir_path} does not exist"))
    else:
        return (0, None)


def get_youtube_data_from_url(url: str) -> YouTube:
    result, value = src.youtube_data.get_youtube_data_from_url(url)
    if result == 0:
        return value
    else:
        raise ValueError(value)


def get_transcript(youtube_video: YouTube) -> str:
    result, value = src.transcript.get_transcript(youtube_video.video_id)
    if result == 0:
        return value
    elif result == 1:
        print("No transcript found", file=stderr)
        generate_result, generate_value = src.transcript.generate_transcript(
            youtube_video
        )
        if generate_result != 0:
            raise src.exceptions.TranscriptGenerationFailed(value)
        return generate_value
    elif result == 2:
        print("Transcripts disabled", file=stderr)
        generate_result, generate_value = src.transcript.generate_transcript(
            youtube_video
        )
        if generate_result != 0:
            raise src.exceptions.TranscriptGenerationFailed(value)
        return generate_value
    else:
        raise NotImplementedError(f"Unhandled result: {result} and value: {value}")


def split_transcript(transcript: str) -> Tuple[str, ...]:
    result, value = src.transcript.split(transcript)
    if result == 1:
        raise ValueError(value)

    return value


def get_ai_content(
    transcript_chunks: Tuple[str, ...], system_message_content: str
) -> str:
    result, value = src.ai.openai_chat(
        system_message=SystemMessage(content=system_message_content),
        temperature=1.0,
        transcript_chunks=transcript_chunks,
    )
    if result != 0:
        raise ValueError(value)

    return value


if __name__ == "__main__":
    ...
