class NoTranscriptFound(Exception):
    def __init__(self, message: str = "No transcript found"):
        super().__init__(message)


class TranscriptsDisabled(Exception):
    def __init__(self, message: str = "Transcripts disabled"):
        super().__init__(message)


class TranscriptGenerationFailed(Exception):
    def __init__(self, message: str = "Transcript generation failed"):
        super().__init__(message)
