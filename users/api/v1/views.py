from django.conf import settings
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, get_object_or_404
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.views import (
    ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken
)
from users.api.v1.permissions import IsUserActive
from users.api.v1.serializers import (
    LoginSerializer, UserSerializer, CreateUserSerializer, UpdatePasswordSerializer
)
from users.models import UserProfile


class Login(ObtainJSONWebToken):
    """
        post: Login user and obtain JWT Token
    """
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )


class Logout(CreateAPIView):
    """
        post: Login user and obtain JWT Token
    """
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(
            settings.JWT_AUTH.get('JWT_AUTH_COOKIE')
        )
        return response


class RetrieveUpdateMe(RetrieveUpdateAPIView):
    """
        get: Return user info

        put: Update user info
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SignUp(CreateAPIView):
    """
        post: Register a new user
    """
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny, )


class ChangePassword(UpdateAPIView):
    """
        put: Update user's password
    """
    serializer_class = UpdatePasswordSerializer
    permission_classes = (IsAuthenticated, IsUserActive, )

    def get_object(self):
        return self.request.user


class DeleteAccount(APIView):
    """
        post: Delete account
    """
    permission_classes = (IsAuthenticated, IsUserActive, )

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
