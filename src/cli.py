#!/usr/bin/env python3
import os
import sys

import click
import slugify

from src.ai import AI
from src.transcript import Transcript


@click.command()
@click.option(
    "--url",
    prompt="The URL of the YouTube video.",
    help="The URL of the YouTube video.",
)
@click.option(
    "--transcript-only",
    is_flag=True,
    help="Print the transcript without further processing",
    default=False,
)
@click.option(
    "--takeaways/--no-takeaways",
    help="Whether or not to include key takeaways in the output",
    default=True,
)
@click.option(
    "--article/--no-article",
    help="Whether or not to include an article form of the transcript in the ouput",
    default=True,
)
@click.option(
    "--metadata/--no-metadata",
    help="Whether or not to include video metadata in the ouput",
    default=True,
)
@click.option(
    "--write", is_flag=True, help="whether or not to write a file", default=False
)
def main(
    url: str,
    transcript_only: bool,
    takeaways: bool,
    article: bool,
    metadata: bool,
    write: bool,
) -> None:
    """
    Main function that processes the command line arguments and
    generates the desired output.

    Args:
        url (str): The URL of the YouTube video.
        transcript_only (bool): Flag indicating whether to output only the transcript.
        takeaways (bool): Flag indicating whether to output the takeaways.
        article (bool): Flag indicating whether to output the article summary.
        metadata (bool): Flag indicating whether to output the video metadata.
        write (bool): Flag indicating whether to write the output to a file.

    Returns:
        None
    """
    transcript = Transcript.get_transcript(url)
    output = []
    if write:
        filename = f"{slugify.slugify(transcript.metadata.title)}.md"
        if os.path.isfile(filename):
            raise FileExistsError(f"{filename} already exists")
        sys.stdout = open(filename, "a")

    if transcript_only:
        output.append(transcript.content)
        takeaways = False
        article = False
        metadata = False

    if any([takeaways, article]):
        ai = AI(transcript)

    if article:
        output.append("".join(ai.summary()))
        output.append("\n---\n")
    if takeaways:
        output.append("".join((ai.takeaways())))
        output.append("\n---\n")
    if metadata:
        output.append(transcript.metadata.print())

    print("".join(output))


if __name__ == "__main__":
    main()
