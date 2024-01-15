class InvalidTranscript(ValueError):
    """Raised when the transcript is not specified."""

    def __init__(self):
        """Initializes the InvalidTranscript exception."""
        super().__init__("The transcript must be specified.")
