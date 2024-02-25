# Generated by CodiumAI

import pytest
from youtube_cheatsheet.exceptions import (
    NoTranscriptFoundError,
    OutputPathValidationError,
    TranscriptsDisabledError,
)


class TestNoTranscriptFound:
    # NoTranscriptFound exception can be caught and handled appropriately
    def test_catch_exception(self):
        """
        Test method to catch NoTranscriptFoundError exception.

        This method uses the `pytest.raises` context manager to catch the `NoTranscriptFoundError` exception.
        It raises the exception and verifies that it is caught.

        :param self: The current instance of the test case.
        :returns: None

        """
        with pytest.raises(NoTranscriptFoundError):
            raise NoTranscriptFoundError


class TestTranscriptsDisabled:
    # TranscriptsDisabled is raised in a try-except block
    def test_try_except_block(self):
        """
        Test a try-except block for raising a specific exception.

        Args:
            self: The current instance of the test.

        Raises:
            TranscriptsDisabledError: If the specified exception is raised with the given error message "Transcripts disabled".

        """
        with pytest.raises(TranscriptsDisabledError, match="Transcripts disabled"):
            raise TranscriptsDisabledError


def test_output_path_validation_error():
    with pytest.raises(OutputPathValidationError, match="Output path validation error"):
        raise OutputPathValidationError
