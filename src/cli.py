#!/usr/bin/env python3
import click
import sys

from src.ai import AI
from src.transcript import Transcript


@click.command()
@click.option(
    "--url",
    prompt="The URL of the YouTube video.",
    help="The URL of the YouTube video.",
)
@click.option("--transcript-only", is_flag=True, help="Print the transcript without further processing", default=False)
@click.option("--takeaways/--no-takeaways", help="Whether or not to include key takeaways in the output", default=True)
@click.option("--article/--no-article", help="Whether or not to include an article form of the transcript in the ouput", default=True)
@click.option("--metadata/--no-metadata", help="Whether or not to include video metadata in the ouput", default=True)
def main(url: str, transcript_only: bool, takeaways: bool, article: bool, metadata: bool):
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
    if transcript_only:
      print(transcript.content)
      sys.exit(0)

    ai = AI(transcript)

    if takeaways:
      ai.print_takeaways()
    if article:
      ai.print_summary()
    if metadata:
      transcript.metadata.print()


if __name__ == "__main__":
    main()
