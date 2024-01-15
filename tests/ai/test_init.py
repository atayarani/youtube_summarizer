from src.ai import AI


class Test__Init__:
    # Initializes an instance of the AI class with a valid transcript.
    def test_valid_transcript(self, valid_transcript):
        ai = AI(valid_transcript)
        assert ai.transcript == "This is the transcript content"
        assert ai.metadata.title == "Transcript Title"
        assert ai.metadata.publish_date == "2022-01-01"
        assert ai.metadata.author == "John Doe"
        assert ai.metadata.url == "https://example.com/transcript"

    # # Raises no exception when a valid transcript is provided.
    # def test_no_exception_valid_transcript(self):
    #     transcript = MockTranscript(content="This is the transcript content", metadata=MockMetadata(title="Transcript Title", publish_date="2022-01-01", author="John Doe", url="https://example.com/transcript"))
    #     try:
    #         ai = AI(transcript)
    #     except Exception as e:
    #         pytest.fail(f"Exception raised: {e}")

    # # Sets the transcript content and metadata attributes correctly.
    # def test_attributes_correctly_set(self):
    #     transcript = MockTranscript(content="This is the transcript content", metadata=MockMetadata(title="Transcript Title", publish_date="2022-01-01", author="John Doe", url="https://example.com/transcript"))
    #     ai = AI(transcript)
    #     assert ai.transcript == "This is the transcript content"
    #     assert ai.metadata.title == "Transcript Title"
    #     assert ai.metadata.publish_date == "2022-01-01"
    #     assert ai.metadata.author == "John Doe"
    #     assert ai.metadata.url == "https://example.com/transcript"

    # # Raises an InvalidTranscript exception when the transcript is not specified.
    # def test_invalid_transcript_exception(self):
    #     with pytest.raises(InvalidTranscript):
    #         ai = AI(MockTranscript(content=None, metadata=MockMetadata(title="Transcript Title", publish_date="2022-01-01", author="John Doe", url="https://example.com/transcript")))

    # # Raises a KeyError exception when the OPENAI_API_KEY environment variable is not set.
    # def test_key_error_exception(self, monkeypatch):
    #     monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    #     with pytest.raises(KeyError):
    #         ai = AI(MockTranscript(content="This is the transcript content", metadata=MockMetadata(title="Transcript Title", publish_date="2022-01-01", author="John Doe", url="https://example.com/transcript")))
