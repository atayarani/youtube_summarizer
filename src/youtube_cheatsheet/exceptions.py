class NoTranscriptFoundError(Exception):
    """
    An exception that is raised when no transcript is found.
    """

    def __init__(self) -> None:
        super().__init__("No transcript found")


class TranscriptsDisabledError(Exception):
    """
    An exception that is raised when transcripts are disabled.
    """

    def __init__(self) -> None:
        super().__init__("Transcripts disabled")


class TranscriptSplitError(Exception):
    """
    An exception that is raised when transcripts are disabled.
    """

    def __init__(self) -> None:
        super().__init__("Transcript must be specified")


class TranscriptGenerationFailedError(Exception):
    """
    An exception that is raised when the generation of a transcript fails.
    """

    def __init__(self, failure) -> None:
        super().__init__(f"Operation failed with error: {failure}")


class OutputPathValidationError(Exception):
    """Custom exception class for output path validation errors."""

    def __init__(self) -> None:
        super().__init__("Output path validation error")


class InvalidModelError(Exception):
    """Custom exception class for invalid model errors."""

    def __init__(self) -> None:
        super().__init__("Invalid model error")


class OpenAIKeyError(Exception):
    def __init__(self) -> None:
        super().__init__("OpenAI API Key is not specified")


class InvalidSystemMessageError(Exception):
    def __init__(self) -> None:
        super().__init__("SystemMessage cannot be blank")


class InvalidURLError(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid YouTube URL")


class MissingMetadataError(Exception):
    def __init__(self) -> None:
        super().__init__("No metadata available for video")
