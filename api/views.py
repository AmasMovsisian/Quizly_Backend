from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.conf import settings


class TokenRefreshView(APIView):
    """
    API view to refresh the access token using a refresh token stored in a cookie.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to refresh the access token.

        Args:
            request: The Django HTTP request object.

        Returns:
            Response: 200 OK with the new access token set in a cookie if successful.
            Response: 401 Unauthorized if the refresh token is missing or invalid.
        """
        refresh_token = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token missing'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            response = Response(
                {'detail': 'Token refreshed'},
                status=status.HTTP_200_OK
            )

            response.set_cookie(
                settings.SIMPLE_JWT['AUTH_COOKIE'],
                new_access_token,
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            )

            return response

        except Exception:
            return Response(
                {'detail': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
