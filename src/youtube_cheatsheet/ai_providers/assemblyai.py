import tempfile

from langchain.docstore.document import Document
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from pytube import YouTube
from returns.pipeline import flow
from returns.result import Failure, Result, Success

import youtube_cheatsheet.video_providers.youtube.audio


def parse_youtube_audio(audio_file: str) -> list[Document]:
    loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)  # pragma: no cover
    return loader.load()  # pragma: no cover


def generate_transcript(video: YouTube) -> Result[str, None]:
    with tempfile.TemporaryDirectory() as save_dir:
        transcript = flow(
            youtube_cheatsheet.video_providers.youtube.audio.fetch_youtube_audio(
                video, save_dir
            ),
            lambda audio_file: parse_youtube_audio(audio_file),
        )

    if len(transcript) == 0:
        return Failure(None)

    return Success(transcript[0].page_content)
