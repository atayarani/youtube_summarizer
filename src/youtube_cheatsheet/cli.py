import pathlib
from typing import Annotated, Optional

import typer
from returns.pipeline import flow

import youtube_cheatsheet.ai_providers.openai
import youtube_cheatsheet.exceptions
import youtube_cheatsheet.output
import youtube_cheatsheet.transcript
import youtube_cheatsheet.video_providers.youtube.data

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
    """
    youtube_video = youtube_cheatsheet.video_providers.youtube.data.YouTubeData()
    transcript_chunks = flow(
        youtube_video.get_from_url(url),
        lambda video: youtube_cheatsheet.transcript.set_transcript_pipe(video),
        youtube_cheatsheet.transcript.split,
    )
    metadata_info = youtube_video.metadata
    if isinstance(metadata_info, youtube_cheatsheet.exceptions.MissingMetadataError):
        print(repr(metadata_info))
        exit(1)
    
    if isinstance(transcript_chunks, youtube_cheatsheet.exceptions.TranscriptSplitError):
        print(repr(transcript_chunks))
        exit(1)

    if metadata_info["title"] is None:
        print("Metadata is missing title")
        exit(1)

    # We pass the boolean values to the methods here, so we don't generate them
    # if the template doesn't need them.  If we do it in the template, which
    # was my original plan, then we may generate data from AI providers for
    # no good reason.
    flow(
        youtube_cheatsheet.output.get_output(
            metadata_info["title"],  
            youtube_data_metadata=youtube_video.metadata_string(metadata),
            output_takeaways=youtube_cheatsheet.ai_providers.openai.get_takeaways(
                takeaways, transcript_chunks
            ),
            output_summary=youtube_cheatsheet.ai_providers.openai.get_summary(
                summary, transcript_chunks
            ),
        ),
        lambda output: youtube_cheatsheet.output.write_file(
            metadata_info["title"],  # type: ignore
            output,
            path,
        )
        if path
        else print(output),
    )


if __name__ == "__main__":
    ...
