"""
Service for audio transcription using Whisper AI.
"""

from pathlib import Path

import whisper

from quizzes.utils.exceptions import TranscriptionError


MODEL_NAME = "base"


def transcribe_audio(audio_path: Path) -> str:
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path: Path to audio file.

    Returns:
        Transcribed text.

    Raises:
        TranscriptionError: If transcription fails.
    """
    try:
        model = whisper.load_model(MODEL_NAME)
        result = model.transcribe(str(audio_path))
    except Exception as error:
        raise TranscriptionError(
            "Audio transcription failed."
        ) from error

    transcript = result.get("text", "").strip()

    if not transcript:
        raise TranscriptionError(
            "No transcript was generated."
        )

    return transcript