"""
Service for audio conversion using FFmpeg.
"""

import subprocess
from pathlib import Path

from quizzes.utils.exceptions import AudioConversionError


def convert_audio_to_wav(audio_path: Path) -> Path:
    """
    Convert audio file to WAV format for Whisper.

    Args:
        audio_path: Path to source audio file.

    Returns:
        Path to converted WAV file.

    Raises:
        AudioConversionError: If conversion fails.
    """
    wav_path = audio_path.with_suffix(".wav")

    command = [
        "ffmpeg",
        "-i",
        str(audio_path),
        "-ar",
        "16000",
        "-ac",
        "1",
        "-y",
        str(wav_path),
    ]

    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as error:
        raise AudioConversionError(
            "Audio conversion failed."
        ) from error

    if not wav_path.exists():
        raise AudioConversionError(
            "Converted audio file was not created."
        )

    return wav_path
