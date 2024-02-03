import pytest

import src.cli


def test_function_succeeds(mocker):
    mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
    mock_transcript_get_transcript.return_value = (0, "foo")
    mock_youtube_video = mocker.patch("pytube.YouTube")
    mock_youtube_video.video_id = "12345"

    assert src.cli.get_transcript(mock_youtube_video) == "foo"


@pytest.mark.parametrize(
    "get_transcript_return_value",
    [pytest.param((1, "foo"), id="not_found"), pytest.param((2, "foo"), id="disabled")],
)
def test_generation_succeeds(mocker, get_transcript_return_value):
    mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
    mock_transcript_get_transcript.return_value = get_transcript_return_value
    mock_youtube_video = mocker.patch("pytube.YouTube")
    mock_youtube_video.video_id = "12345"
    mock_transcript_generate_transcript = mocker.patch(
        "src.transcript.generate_transcript"
    )
    mock_transcript_generate_transcript.return_value = (0, "foo")

    src.cli.get_transcript(mock_youtube_video)

    mock_transcript_generate_transcript.assert_called_once_with(mock_youtube_video)


def test_generated_transcript_not_found(mocker):
    mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
    mock_transcript_get_transcript.return_value = (1, "foo")
    mock_youtube_video = mocker.patch("pytube.YouTube")
    mock_youtube_video.video_id = "12345"
    mock_transcript_generate_transcript = mocker.patch(
        "src.transcript.generate_transcript"
    )
    mock_transcript_generate_transcript.return_value = (1, "foo")

    with pytest.raises(src.exceptions.TranscriptGenerationFailed):
        src.cli.get_transcript(mock_youtube_video)

    mock_transcript_generate_transcript.assert_called_once_with(mock_youtube_video)


def test_transcripts_disabled(mocker):
    mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
    mock_transcript_get_transcript.return_value = (2, "foo")
    mock_youtube_video = mocker.patch("pytube.YouTube")
    mock_youtube_video.video_id = "12345"
    mock_transcript_generate_transcript = mocker.patch(
        "src.transcript.generate_transcript"
    )

    mock_transcript_generate_transcript.return_value = (1, "foo")

    with pytest.raises(src.exceptions.TranscriptGenerationFailed):
        src.cli.get_transcript(mock_youtube_video)

    mock_transcript_generate_transcript.assert_called_once_with(mock_youtube_video)


# def test_generation_succeeded(self, mocker):
#     mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
#     mock_transcript_get_transcript.return_value = (2, "foo")
#     mock_youtube_video = mocker.patch("pytube.YouTube")
#     mock_youtube_video.video_id = "12345"
#     mock_transcript_generate_transcript = mocker.patch(
#         "src.transcript.generate_transcript"
#     )
#     mock_transcript_generate_transcript.return_value = (0, "foo")

#     src.cli.get_transcript(mock_youtube_video)

#     mock_transcript_generate_transcript.assert_called_once_with(mock_youtube_video)


def test_not_implemented_error(mocker):
    mock_transcript_get_transcript = mocker.patch("src.transcript.get_transcript")
    mock_transcript_get_transcript.return_value = (99, "foo")
    mock_youtube_video = mocker.patch("pytube.YouTube")
    mock_youtube_video.video_id = "12345"

    with pytest.raises(NotImplementedError):
        src.cli.get_transcript(mock_youtube_video)
