from django.contrib.auth import get_user_model, login, logout
from django.contrib.sites import requests
from rest_framework import generics, status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer

USER_MODEL = get_user_model()


class RegistrationView(generics.CreateAPIView):
    """регистрация нового пользователя"""
    model = USER_MODEL
    serializer_class = RegistrationSerializer


class LoginView(GenericAPIView):
    """Ввод логина"""
    serializer_class = LoginSerializer

    def post(self, request: requests, *args: str, **kwargs: int) -> Response:
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user=user)
        user_serializer = ProfileSerializer(instance=user)
        return Response(user_serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Отображения профайла пользователя"""
    serializer_class = ProfileSerializer
    queryset = USER_MODEL.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(generics.UpdateAPIView):
    """смена пароля"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user
