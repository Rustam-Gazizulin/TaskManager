from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers


USER_MODEL = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.get('password')
        password_repeat = validated_data.pop('password')

        if password != password_repeat:
            raise serializers.ValidationError('Passwords do not match')

        validated_data['password'] = make_password(password)
        instance = super().create(validated_data)
        return instance


    class Meta:
        model = USER_MODEL
        fields = '__all__'