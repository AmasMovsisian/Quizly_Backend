from rest_framework import serializers
from quizzes.models import Quiz, Question


class StandardQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer']


class QuizSerializer(serializers.ModelSerializer):
    questions = StandardQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']
        read_only_fields = ['user', 'created_at', 'updated_at']


class PostQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']


class PostQuizSerializer(serializers.ModelSerializer):
    questions = PostQuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions']
        read_only_fields = ['user', 'created_at', 'updated_at']