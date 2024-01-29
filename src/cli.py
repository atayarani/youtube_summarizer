#!/usr/bin/env python3
import os.path

import slugify
import typer
from jinja2 import Template
from typer import BadParameter
from typing_extensions import Annotated

from src.ai import AI
from src.metadata import Metadata
from src.transcript import Transcript
from src.youtube_data import YouTubeData

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
    write: Annotated[
        bool, typer.Option("--write", help="Write the output to a file")
    ] = False,
    path: Annotated[
        str, typer.Option(help="The path to write the output file to")
    ] = ".",
) -> None:
    """
    Main function to process YouTube video and generate summary.

    Args:
        url (str): The URL of the YouTube video.
        takeaways (bool): Flag indicating whether to generate takeaways from the video.
        summary (bool): Flag indicating whether to generate a summary.
        metadata (bool): Flag indicating whether to print video metadata.
        write (bool): Flag indicating whether to write the output to a file.
        path (str): The path to write the output file.

    Returns:
        None
    """
    youtube_data = get_youtube_data(url)
    transcript = get_transcript(youtube_data)

    if any([takeaways, summary]):
        ai = AI(transcript, youtube_data)

    output_dict = {
        "title": youtube_data.metadata.title,
        "output_takeaways": ai.takeaways() if takeaways else None,
        "output_summary": ai.summary() if summary else None,
        "youtube_data_metadata": str(youtube_data.metadata) if metadata else None,
    }

    output = get_output(output_dict)

    if write:
        filename = slugify_video_title(youtube_data.metadata)
        write_file(filename, output, path)
    else:
        print(output)


def get_output(output_dict: dict[str, str | None]) -> str:
    template_str = (
        "{{ youtube_data_metadata.title }}\n"
        "{% if output_summary %}{{ output_summary }}\n---\n{% endif %}"
        "{% if output_takeaways %}{{ output_takeaways }}\n---\n{% endif %}"
        "{% if youtube_data_metadata %}{{ youtube_data_metadata }}{% endif %}"
    )

    template = Template(template_str)
    return template.render(**output_dict)


def slugify_video_title(youtube_data_metadata: Metadata) -> str:
    return slugify.slugify(youtube_data_metadata.title)


def write_file(filename: str, content: str, path: str) -> None:
    file = os.path.join(path, f"{filename}.md")
    if os.path.isfile(file):
        raise FileExistsError(f"{file} already exists")
    else:
        with open(file, "w") as f:
            f.write(content)


def get_youtube_data(url: str) -> YouTubeData:
    try:
        return YouTubeData(url.split("&")[0])
    except BadParameter:
        exit("Invalid YouTube URL")


def get_transcript(youtube_data: YouTubeData) -> Transcript:
    return Transcript(youtube_data)


if __name__ == "__main__":
    ...
