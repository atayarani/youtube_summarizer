import pytube


def fetch_youtube_audio(video: pytube.YouTube, save_dir: str) -> str:
    audio = video.streams.filter(only_audio=True).first()
    return str(audio.download(output_path=save_dir))
