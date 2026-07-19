from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        confirmed_password = request.data.get('confirmed_password')
        email = request.data.get('email')

        if not username or not password or not email or not confirmed_password:
            return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != confirmed_password:
            return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.create_user(username=username, email=email, password=password)
            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({"detail": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            
            response = Response({
                "detail": "Login successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)
            
            cookie_secure = settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False)
            cookie_httponly = settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True)
            cookie_samesite = settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax')
            
            response.set_cookie(
                settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token'),
                str(refresh.access_token),
                httponly=cookie_httponly,
                secure=cookie_secure,
                samesite=cookie_samesite
            )
            response.set_cookie(
                settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'),
                str(refresh),
                httponly=cookie_httponly,
                secure=cookie_secure,
                samesite=cookie_samesite
            )
            return response
            
        return Response({"detail": "Invalid login details."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({
            "detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."
        }, status=status.HTTP_200_OK)
        
        response.delete_cookie(settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token'))
        response.delete_cookie(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
        return response


class TokenRefreshCookieView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', 'refresh_token'))
        if not refresh_token:
            return Response({"detail": "Refresh token invalid or missing."}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            refresh = RefreshToken(refresh_token)
            response = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)
            
            response.set_cookie(
                settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token'),
                str(refresh.access_token),
                httponly=settings.SIMPLE_JWT.get('AUTH_COOKIE_HTTP_ONLY', True),
                secure=settings.SIMPLE_JWT.get('AUTH_COOKIE_SECURE', False),
                samesite=settings.SIMPLE_JWT.get('AUTH_COOKIE_SAMESITE', 'Lax')
            )
            return response
        except Exception:
            return Response({"detail": "Refresh token invalid or missing."}, status=status.HTTP_401_UNAUTHORIZED)