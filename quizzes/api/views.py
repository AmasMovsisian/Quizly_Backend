import traceback
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quizzes.models import Quiz, Question
from .serializers import QuizSerializer, PostQuizSerializer
from quizzes.services.quiz_service import create_quiz


class QuizViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing quizzes. Supports CRUD operations with JWT authentication.
    All actions are restricted to authenticated users.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only quizzes belonging to the authenticated user.

        Returns:
            QuerySet: Filtered Quiz queryset for the current user.
        """
        return Quiz.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.

        Returns:
            SerializerClass: PostQuizSerializer for create action, otherwise QuizSerializer.
        """
        if self.action == 'create':
            return PostQuizSerializer
        return QuizSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new quiz from a URL. The quiz is generated asynchronously
        and associated with the authenticated user.

        Args:
            request: The Django HTTP request object containing the 'url' field.

        Returns:
            Response: 201 Created with serialized quiz data on success.
            Response: 400 Bad Request if URL is missing.
            Response: 500 Internal Server Error on unexpected failure.
        """
        url = request.data.get('url')
        if not url:
            return Response(
                {'error': 'Invalid URL or request data.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quiz = create_quiz(
                url,
                request.user,
            )

            serializer = self.get_serializer(quiz)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("\n" + "="*50)
            print("CRITICAL ERROR DURING QUIZ CREATION:")
            print(str(e))
            traceback.print_exc()
            print("="*50 + "\n")

            return Response(
                {'error': 'Internal server error.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an existing quiz.

        Args:
            request: The Django HTTP request object.

        Returns:
            Response: Updated quiz data.
        """
        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a quiz instance.

        Args:
            request: The Django HTTP request object.

        Returns:
            Response: 204 No Content on successful deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(None, status=status.HTTP_204_NO_CONTENT)