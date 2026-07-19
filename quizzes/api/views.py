import traceback
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quizzes.models import Quiz, Question
from .serializers import QuizSerializer, PostQuizSerializer


class QuizViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostQuizSerializer
        return QuizSerializer
    
    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        if not url:
            return Response(
                {'error': 'Invalid URL or request data.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            quiz = Quiz.objects.create(
                user=request.user,
                title="Quiz Title",
                description="Quiz Description",
                video_url=url
            )
            
            Question.objects.create(
                quiz=quiz,
                question_title="Question 1",
                question_options=["Option A", "Option B", "Option C", "Option D"],
                answer="Option A"
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
        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(None, status=status.HTTP_204_NO_CONTENT)