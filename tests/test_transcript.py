import langchain
import lorem
import pytest
import youtube_transcript_api

from src.transcript import get_transcript, split


class TestGetTranscript:
    def test_success(self, mocker):
        mock_transcript_api = mocker.patch(
            "youtube_transcript_api.YouTubeTranscriptApi"
        )
        mock_transcript_api.get_transcript.side_effect = None
        mock_transcript_api.get_transcript.return_value = [
            {"text": "bar"},
            {"text": "baz"},
        ]

        result, value = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")
        assert result == 0
        assert value == "bar baz"

    def test_not_found(self, mocker):
        mock_transcript_api = mocker.patch(
            "youtube_transcript_api.YouTubeTranscriptApi"
        )
        mock_transcript_api.get_transcript.side_effect = (
            youtube_transcript_api._errors.NoTranscriptFound("foo", ["en"], "bar baz")
        )
        mock_transcript_api.get_transcript.return_value = [
            {"text": "bar"},
            {"text": "baz"},
        ]

        result, value = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")
        assert result == 1
        assert value == "No transcript found"

    def test_disabled(self, mocker):
        mock_transcript_api = mocker.patch(
            "youtube_transcript_api.YouTubeTranscriptApi"
        )
        mock_transcript_api.get_transcript.side_effect = (
            youtube_transcript_api._errors.TranscriptsDisabled("foo")
        )
        mock_transcript_api.get_transcript.return_value = [
            {"text": "bar"},
            {"text": "baz"},
        ]

        result, value = get_transcript("foo")

        mock_transcript_api.get_transcript.assert_called_once_with("foo")
        assert result == 2
        assert value == "Transcripts disabled"


class TestSplit:
    def test_function_succeeds_with_one_chunk(self, mocker):
        # mock_char_split = mocker.patch("langchain.text_splitter")

        # result, value = split(" ".join(loremipsum.get_paragraphs(20)))
        result, value = split("foo bar")
        assert result == 0
        assert value == ("foo bar",)

    def test_function_succeeds_with_multiple_chunks(self, mocker):
        input = lorem.get_word(20000)

        result, value = split(input)
        print(result)
        print(value)
        # print(value)
        # assert result == 0
        # mock_char_split = mocker.patch("langchain.text_splitter")
        # mock_char_split.split_text.return_value = ["foo", "bar"]

        # mock_split = mocker.patch("src.transcript.split")
        # mock_split.return_value = (0, tuple(("foo", "bar")))
        # result, value = split(loremipsum.get_paragraphs(20))
        # print(len(value))
        # print(result)

        # assert split("") == ("foo", "bar")
