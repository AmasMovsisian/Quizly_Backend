"""
Validation helper functions for quizzes.
"""

from urllib.parse import urlparse

from rest_framework.exceptions import ValidationError


VALID_HOSTS = (
    "youtube.com",
    "www.youtube.com",
    "youtu.be",
    "www.youtu.be",
)


def validate_youtube_url(url: str) -> str:
    """
    Validate a YouTube URL.

    Args:
        url: URL submitted by the user.

    Returns:
        Validated URL.

    Raises:
        ValidationError: If the URL is invalid.
    """
    parsed_url = urlparse(url)

    if not parsed_url.scheme:
        raise ValidationError("URL is required.")

    if parsed_url.netloc not in VALID_HOSTS:
        raise ValidationError("Only YouTube URLs are allowed.")

    return url
