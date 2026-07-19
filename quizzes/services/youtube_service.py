"""
Service for downloading YouTube audio files.
"""

import uuid
from pathlib import Path

from django.conf import settings
from yt_dlp import YoutubeDL

from quizzes.utils.exceptions import AudioDownloadError


DOWNLOAD_DIR = Path(settings.MEDIA_ROOT) / "downloads"
DOWNLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def download_audio(url: str) -> Path:
    """
    Download audio from YouTube.

    Args:
        url: YouTube video URL.

    Returns:
        Downloaded audio path.

    Raises:
        AudioDownloadError: If download fails.
    """
    file_id = str(uuid.uuid4())

    output_template = str(
        DOWNLOAD_DIR / file_id
    )

    options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        },
        "extractor_args": {
            "youtube": {
                "player_client": [
                    "android"
                ]
            }
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with YoutubeDL(options) as youtube:
            youtube.download([url])

    except Exception as error:
        raise AudioDownloadError(
            "Failed to download YouTube audio."
        ) from error

    audio_path = DOWNLOAD_DIR / f"{file_id}.mp3"

    if not audio_path.exists():
        raise AudioDownloadError(
            "Audio file was not created."
        )

    return audio_path