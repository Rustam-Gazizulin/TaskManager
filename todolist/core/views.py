from django.contrib.auth import get_user_model, login

from rest_framework import generics
from rest_framework.response import Response

from .serializers import RegistrationSerializer, LoginSerializer

USER_MODEL = get_user_model()


class RegistrationView(generics.CreateAPIView):
    model = USER_MODEL
    serializer_class = RegistrationSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)
