class NoTranscriptFoundError(Exception):
    """
    An exception that is raised when no transcript is found.

    Args:
        message (str, optional): A custom message describing the error. Defaults to "No transcript found".

    Raises:
        NoTranscriptFoundError: Raised when no transcript is found.
    """

    def __init__(self, message: str = "No transcript found"):
        """
        Raise when no transcript is found.

        Args:
            message (str): Optional. The message to be displayed when no transcript is found. Default is "No transcript found".

        """
        super().__init__(message)


class TranscriptsDisabledError(Exception):
    """
    An exception that is raised when transcripts are disabled.

    Args:
        message (str, optional): A custom message describing the error. Defaults to "Transcripts disabled".

    Raises:
        TranscriptsDisabledError: Raised when transcripts are disabled.
    """

    def __init__(self, message: str = "Transcripts disabled"):
        """
        Raise when transcripts are disabled.

        Args:
            message (str): The message to be displayed. Defaults to "Transcripts disabled".

        """
        super().__init__(message)


class TranscriptGenerationFailedError(Exception):
    """
    An exception that is raised when the generation of a transcript fails.

    Args:
        message (str, optional): A custom message describing the error. Defaults to "Transcript generation failed".

    Raises:
        TranscriptGenerationFailedError: Raised when the generation of a transcript fails.
    """

    def __init__(self, failure):
        """
        Raise when the generation of a transcript fails.

        Args:
            failure (str): The error message indicating the failure of the operation.

        """
        super().__init__(f"Operation failed with error: {failure}")


class OutputPathValidationError(Exception):
    """Custom exception class for output path validation errors."""

    def __init__(self):
        """
        Initialize an instance of the class and sets the error message for output path validation error.

        Parameters:
            self : object
                An instance of the class.

        Returns:
            None
        """
        super().__init__("Output path validation error")


class InvalidModelError(Exception):
    """Custom exception class for invalid model errors."""

    def __init__(self):
        """Initialize an instance of the class and sets the error message for invalid model error."""
        super().__init__("Invalid model error")
