import pytest

from src.ai import AI


class Test_SplitTranscript:
    # Returns a list of transcript chunks when given a valid transcript.
    def test_valid_transcript(self, valid_transcript):
        ai = AI(valid_transcript)
        chunks = ai._split_transcript()
        assert isinstance(chunks, list)
        assert len(chunks) > 0

    # Returns a list with a single chunk when given a transcript shorter than the chunk size.
    def test_short_transcript(self, short_transcript):
        ai = AI(short_transcript)
        chunks = ai._split_transcript()
        assert isinstance(chunks, list)
        assert len(chunks) == 1

    # Raises a TypeError when given a transcript that is not a string.
    def test_non_string_transcript(self, invalid_type_transcript):
        with pytest.raises(TypeError):
            ai = AI(invalid_type_transcript)
            ai._split_transcript()
