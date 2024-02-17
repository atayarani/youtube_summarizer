from types import MappingProxyType

from pytube import YouTube


def set_metadata(video: YouTube) -> MappingProxyType[str, str]:
    r"""
    Set metadata for a YouTube video.

    Args:
      video: The YouTube video to set metadata for.
      video: YouTube:

    Returns:
      MappingProxyType[str, str]: A mapping of the video's metadata, as follows:
      - "title": The title of the video.
      - "publish_date": The publish date of the video in the format "YYYY-MM-DD".
      - "author": The author of the video.
      - "url": The URL of the video.
      - "description": The description of the video, with each line indented by a tab ('\t').
      - "video_id": The ID of the video.
    """
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


def metadata_string(metadata_info: MappingProxyType[str, str]) -> str:
    """
    Convert a read-only dictionary-like object (MappingProxyType) containing metadata information into a string.

    Args:
      metadata_info: A read-only dictionary-like object (MappingProxyType) containing metadata information.


    Returns:
      A string representation of the metadata, excluding the "video_id" key, formatted as "<key>: <value>" separated by newlines.

    """
    return "\n".join([f"{k}: {v}" for k, v in metadata_info.items() if k != "video_id"])
