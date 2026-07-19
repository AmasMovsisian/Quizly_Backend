"""
Service for creating and storing quizzes.
"""

from django.db import transaction

from quizzes.models import Quiz, Question

from quizzes.services.ffmpeg_service import convert_audio_to_wav
from quizzes.services.gemini_service import generate_quiz
from quizzes.services.whisper_service import transcribe_audio
from quizzes.services.youtube_service import download_audio

from quizzes.utils.validators import validate_youtube_url


@transaction.atomic
def create_quiz(url: str, user) -> Quiz:
    """
    Create quiz from YouTube URL.

    Args:
        url: YouTube video URL.
        user: Authenticated user.

    Returns:
        Created quiz instance.
    """
    youtube_url = validate_youtube_url(url)

    audio_file = download_audio(youtube_url)

    wav_file = convert_audio_to_wav(audio_file)

    transcript = transcribe_audio(wav_file)

    quiz_data = generate_quiz(transcript)

    return save_quiz(
        quiz_data,
        youtube_url,
        user,
    )


def save_quiz(
    quiz_data: dict,
    video_url: str,
    user,
) -> Quiz:
    """
    Save quiz data into database.

    Args:
        quiz_data: Generated Gemini JSON.
        video_url: YouTube URL.
        user: Quiz owner.

    Returns:
        Saved quiz.
    """
    quiz = Quiz.objects.create(
        user=user,
        title=quiz_data["title"],
        description=quiz_data["description"],
        video_url=video_url,
    )

    save_questions(
        quiz,
        quiz_data["questions"],
    )

    return quiz


def save_questions(
    quiz: Quiz,
    questions: list,
) -> None:
    """
    Save quiz questions.

    Args:
        quiz: Quiz instance.
        questions: Generated questions.
    """
    question_list = []

    for item in questions:
        question_list.append(
            Question(
                quiz=quiz,
                question_title=item["question_title"],
                question_options=item["question_options"],
                answer=item["answer"],
            )
        )

    Question.objects.bulk_create(question_list)