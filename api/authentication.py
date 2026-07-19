from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class CookieJWTAuthentication(JWTAuthentication):
    """
    JWT authentication class that extracts the token from an HTTP cookie
    instead of the Authorization header.
    """

    def authenticate(self, request):
        """
        Authenticate the request using a JWT token from a cookie.

        Args:
            request: The Django HTTP request object.

        Returns:
            tuple: (user, validated_token) if authentication is successful.
            None: If no token is present in the cookie.

        Raises:
            AuthenticationFailed: If the token is invalid or expired.
        """
        cookie_name = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token')
        raw_token = request.COOKIES.get(cookie_name)

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed(f"Authentication error: {str(e)}")
