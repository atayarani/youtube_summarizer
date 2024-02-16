import pytube


def get_youtube_data_from_url(url: str) -> tuple[int, pytube.YouTube | str]:
    """
    Get a YouTube video object from the given URL.

    Args:
        url: The URL of the YouTube video.

    Returns:
        A tuple containing an integer status code and either a pytube.YouTube object representing the video or a string with an error message.

    Raises:
        None

    Example:
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        status, data = get_youtube_data_from_url(url)
        if status == 0:
            print(f"Video title: {data.title}")
        else:
            print(f"Error: {data}")
    """
    try:
        video = pytube.YouTube(url.split("&")[0])
        video.check_availability()  # pragma: no cover
    except pytube.exceptions.RegexMatchError:
        return 1, "Invalid YouTube URL"
    else:
        return 0, video


# class YouTubeData:
#     # def __init__(self, url: str):
#     #     """
#     #     Initialize the object with the given URL.

#     #     Args:
#     #         url (str): The URL of the video.
#     #     """
#     #     self._url = url
#     #     self.video: YouTube = self._get_video()

#     # @property
#     # def url(self) -> str:
#     #     return self._url

#     @property
#     def metadata(self) -> Metadata:
#         return Metadata(
#             title=self.video.title,
#             publish_date=self.video.publish_date.strftime("%Y-%m-%d"),
#             author=self.video.author,
#             url=self.video.watch_url,
#             description=self.description,
#             video_id=self.video.video_id,
#         )

#     # @lru_cache
#     # def _get_video(self) -> YouTube:
#     #     """
#     #     Set the video property with the given URL.

#     #     Args:
#     #         url (str): The URL of the video.

#     #     Returns:
#     #         YouTube: The YouTube object representing the video.

#     #     Raises:
#     #         RegexMatchError: If the URL does not match the expected format.
#     #     """
#     #     try:
#     #         video = YouTube(self.url)
#     #         video.check_availability()  # pragma: no cover
#     #     except RegexMatchError:
#     #         raise BadParameter("Invalid YouTube URL")

#     # return video

#     @property
#     def description(self) -> str:
#         """
#         Get the description of the video as a single string.
#         """
