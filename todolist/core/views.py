from django.contrib.auth import get_user_model
from rest_framework import generics


from .serializers import RegistrationSerializer

USER_MODEL = get_user_model()


class RegistrationView(generics.CreateAPIView):
    model = USER_MODEL
    serializer_class = RegistrationSerializer
