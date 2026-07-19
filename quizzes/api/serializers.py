from rest_framework import serializers
from quizzes.models import Quiz, Question


class StandardQuestionSerializer(serializers.ModelSerializer):
    """Serializer for standard Question model representation."""

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for Quiz model with nested read-only questions."""

    questions = StandardQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']
        read_only_fields = ['user', 'created_at', 'updated_at']


class PostQuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model used in POST operations."""

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']


class PostQuizSerializer(serializers.ModelSerializer):
    """Serializer for Quiz model used in POST operations with nested questions."""

    questions = PostQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']
        read_only_fields = ['user', 'created_at', 'updated_at']