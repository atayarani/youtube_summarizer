from src.ai import AI


class TestSummary:
    # Generates a summary of the transcript when provided with a valid transcript and metadata.
    def test_valid_transcript_and_metadata(self, mocker, valid_transcript):
        # Mock the necessary dependencies
        transcript = valid_transcript
        mocker.patch.object(AI, "_split_transcript", return_value=["This is a chunk"])
        mocker.patch.object(AI, "_chat", return_value=["Generated summary"])

        # Initialize the AI object
        ai = AI(transcript)

        # Call the summary method
        result = ai.summary()

        # Assert the result
        assert result == ["Generated summary"]

    # Returns a list of strings representing the generated summary.
    def test_return_type(self, mocker, valid_transcript):
        # Mock the necessary dependencies
        transcript = valid_transcript
        mocker.patch.object(AI, "_split_transcript", return_value=["This is a chunk"])
        mocker.patch.object(AI, "_chat", return_value=["Generated summary"])

        # Initialize the AI object
        ai = AI(transcript)

        # Call the summary method
        result = ai.summary()

        # Assert the return type
        assert isinstance(result, list)

    # Uses a character-based text splitter to split the transcript into chunks.
    def test_text_splitter(self, mocker, valid_transcript):
        # Mock the necessary dependencies
        transcript = valid_transcript
        mocker.patch.object(AI, "_split_transcript", return_value=["This is a chunk"])
        mocker.patch.object(AI, "_chat", return_value=["Generated summary"])

        # Initialize the AI object
        ai = AI(transcript)

        # Call the summary method
        ai.summary()

        # Assert that the text splitter is called
        AI._split_transcript.assert_called_once()
