from types import MappingProxyType

from pytube import YouTube


def set_metadata(video: YouTube) -> MappingProxyType[str, str]:
    video.streams.first()
    return MappingProxyType(
        {
            "title": video.title,
            "publish_date": video.publish_date.strftime("%Y-%m-%d"),
            "author": video.author,
            "url": video.watch_url,
            "description": "".join([f"\n\t{x}" for x in video.description.split("\n")]),
            "video_id": video.video_id,
        }
    )
