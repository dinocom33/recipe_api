"""
Views for the User API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.settings import api_settings
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['User'])
class UserCreateView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


@extend_schema(tags=['User'])
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


@extend_schema(tags=['User'])
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""

        return self.request.user
