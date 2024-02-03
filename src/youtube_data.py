import pytube


def get_youtube_data_from_url(url: str) -> tuple[int, pytube.YouTube | str]:
    try:
        video = pytube.YouTube(url.split("&")[0])
        video.check_availability()  # pragma: no cover
        return (0, video)
    except pytube.exceptions.RegexMatchError:
        return (1, "Invalid YouTube URL")


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
