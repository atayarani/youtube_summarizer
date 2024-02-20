# import pytest
# import youtube_cheatsheet.cli
# from returns.result import Failure, Success


# def test_function_succeeds(mocker):
#     """
#     Verify that the `youtube_cheatsheet.cli.get_transcript()` function returns successful results.

#     Args:
#         mocker: Instance of mocker object from the pytest-mock library.

#     Returns:
#         None
#     """
#     mock_transcript_get_transcript = mocker.patch(
#         "youtube_cheatsheet.transcript.get_transcript"
#     )
#     mock_transcript_get_transcript.return_value = Success("foo")
#     mock_youtube_video = mocker.patch("pytube.YouTube")
#     mock_youtube_video.video_id = "12345"

#     assert youtube_cheatsheet.cli.get_transcript(mock_youtube_video) == Success("foo")


# @pytest.mark.parametrize(
#     "get_transcript_return_value",
#     [pytest.param(Failure("Foo"), id="not_found")],
# )
# def test_generation_succeeds(mocker, get_transcript_return_value):
#     """
#     Test whether the function successfully generates a transcript using the given mock objects and parameters.

#     Args:
#         mocker: The mocker object used for mocking and patching functions and objects.
#         get_transcript_return_value: The return value for the mocked `get_transcript` function.

#     Example usage:
#         mocker = pytest_mock.MockFixture()
#         get_transcript_return_value = (1, "foo")
#         test_generation_succeeds(mocker, get_transcript_return_value)
#     """
#     mock_transcript_get_transcript = mocker.patch(
#         "youtube_cheatsheet.transcript.get_transcript"
#     )
#     mock_transcript_get_transcript.return_value = get_transcript_return_value
#     mock_youtube_video = mocker.patch("pytube.YouTube")
#     mock_youtube_video.video_id = "12345"
#     mock_fetch_youtube_audio = mocker.patch(
#         "youtube_cheatsheet.transcript.fetch_youtube_audio"
#     )
#     mock_fetch_youtube_audio.return_value = "foo"
#     mock_parse_youtube_audio = mocker.patch(
#         "youtube_cheatsheet.transcript.parse_youtube_audio"
#     )
#     mock_parse_youtube_audio.return_value = ""

#     with pytest.raises(youtube_cheatsheet.exceptions.TranscriptGenerationFailedError):
#         youtube_cheatsheet.cli.get_transcript(mock_youtube_video)


# # def test_generated_transcript_not_found(mocker):
# #     """
# #     Test method to check if an exception is raised when the generated transcript is not found.

# #     Args:
# #         mocker: A pytest-mock mocker object to create and handle mock objects.

# #     """
# #     mock_transcript_get_transcript = mocker.patch(
# #         "youtube_cheatsheet.transcript.get_transcript"
# #     )
# #     mock_transcript_get_transcript.return_value = Failure("foo")
# #     mock_youtube_video = mocker.patch("pytube.YouTube")
# #     mock_youtube_video.video_id = "12345"
# #     mock_fetch_youtube_audio = mocker.patch(
# #         "youtube_cheatsheet.transcript.fetch_youtube_audio"
# #     )
# #     mock_fetch_youtube_audio.return_value = "foo"
# #     mock_parse_youtube_audio = mocker.patch(
# #         "youtube_cheatsheet.transcript.parse_youtube_audio"
# #     )
# #     mock_parse_youtube_audio.return_value = ""

# #     with pytest.raises(youtube_cheatsheet.exceptions.TranscriptGenerationFailedError):
# #         youtube_cheatsheet.cli.get_transcript(mock_youtube_video)


# # def test_not_implemented_error(mocker):
# #     """
# #     Test the behavior when the youtube_cheatsheet.cli.get_transcript method is not implemented.

# #     Args:
# #         mocker: an instance of the mocker class used for mocking

# #     Raises:
# #         NotImplementedError: if the youtube_cheatsheet.cli.get_transcript method is not implemented
# #     """
# #     mock_transcript_get_transcript = mocker.patch(
# #         "youtube_cheatsheet.transcript.get_transcript"
# #     )
# #     mock_transcript_get_transcript.return_value = (99, "foo")
# #     mock_youtube_video = mocker.patch("pytube.YouTube")
# #     mock_youtube_video.video_id = "12345"

# #     with pytest.raises(NotImplementedError):
# #         youtube_cheatsheet.cli.get_transcript(mock_youtube_video)
