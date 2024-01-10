#!/usr/bin/env python3
import click

from ai import AI
from transcript import Transcript


@click.command()
@click.option(
    "--url",
    prompt="The URL of the YouTube video.",
    help="The URL of the YouTube video.",
)
def main(url: str):
    """
    This function takes a URL as input and performs the following steps:
    1. Retrieves the transcript for the given URL.
    2. Initializes an AI object with the transcript content.
    3. Prints the AI's output.
    4. Prints the metadata of the transcript.

    Args:
        url (str): The URL of the YouTube video.
    """
    transcript = Transcript.get_transcript(url)
    ai = AI(transcript.content)
    ai.print()
    transcript.metadata.print()


if __name__ == "__main__":
    main()
