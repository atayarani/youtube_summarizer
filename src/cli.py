#!/usr/bin/env python3
import os.path
from sys import stderr

import slugify
import typer
from jinja2 import Template
from pytube import YouTube
from typing_extensions import Annotated

import src.transcript
import src.youtube_data
from src.ai import AI
from src.data import Transcript, TranscriptChunks, YouTubeVideo
from src.metadata import Metadata
from src.transcript import generate_transcript

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

    youtube_video = YouTubeVideo(get_youtube_data_from_url(url)).data
    transcript = Transcript(get_transcript(youtube_video)).data
    transcript_chunks = TranscriptChunks(split_transcript(transcript)).data
    metadata_info = set_metadata(youtube_video)

    if any([takeaways, summary]):
        ai = AI(transcript_chunks, metadata_info)

    output = get_output(
        metadata_info.title,
        metadata=str(metadata_info) if metadata else None,
        takeaways=ai.takeaways() if takeaways else None,
        summary=ai.summary() if summary else None,
    )

    if write:
        filename = slugify_video_title(metadata_info.title)
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
        "{{ title }}\n"
        "{% if output_summary %}{{ output_summary }}\n---\n{% endif %}"
        "{% if output_takeaways %}{{ output_takeaways }}\n---\n{% endif %}"
        "{% if youtube_data_metadata %}{{ youtube_data_metadata }}{% endif %}"
    )

    template = Template(template_str)
    return template.render(**output_dict)


def slugify_video_title(title: str) -> str:
    return slugify.slugify(title)


def write_file(filename: str, content: str, path: str) -> None:
    file = os.path.join(path, f"{filename}.md")
    if os.path.isfile(file):
        raise FileExistsError(f"{file} already exists")
    else:
        with open(file, "w") as f:
            f.write(content)


def get_youtube_data_from_url(url: str) -> YouTube:
    result, value = src.youtube_data.get_youtube_data_from_url(url)
    if result == 0:
        return value
    else:
        print(value)
        exit(1)


def get_transcript(youtube_video: YouTube) -> str:
    result, value = src.transcript.get_transcript(youtube_video.video_id)
    if result == 0:
        return value
    elif result == 1:
        print("No transcript found", file=stderr)
        return generate_transcript(youtube_video)
    elif result == 2:
        print("Transcripts disabled", file=stderr)
        return generate_transcript(youtube_video)
    else:
        raise NotImplementedError(f"Unhandled result: {result} and value: {value}")


def split_transcript(transcript: str) -> list[str]:
    result, value = src.transcript.split(transcript)
    if result == 0:
        return value
    else:
        print(value)
        exit(1)


def set_metadata(video: YouTube) -> Metadata:
    video.streams.first()
    return Metadata(
        title=video.title,
        publish_date=video.publish_date.strftime("%Y-%m-%d"),
        author=video.author,
        url=video.watch_url,
        description="".join([f"\n\t{x}" for x in video.description.split("\n")]),
        video_id=video.video_id,
    )


if __name__ == "__main__":
    ...
