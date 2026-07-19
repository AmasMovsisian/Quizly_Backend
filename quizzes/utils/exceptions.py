"""
Custom exceptions for the quizzes application.
"""


class InvalidYoutubeUrlError(Exception):
    """Raised when the provided URL is not a valid YouTube URL."""


class AudioDownloadError(Exception):
    """Raised when the YouTube audio download fails."""


class AudioConversionError(Exception):
    """Raised when FFmpeg cannot convert the audio."""


class TranscriptionError(Exception):
    """Raised when Whisper fails to transcribe audio."""


class GeminiGenerationError(Exception):
    """Raised when Gemini cannot generate a valid quiz."""


class InvalidQuizJsonError(Exception):
    """Raised when Gemini returns an invalid quiz JSON."""