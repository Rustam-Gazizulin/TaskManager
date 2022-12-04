from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


USER_MODEL = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': e.messages})

        if password != password_repeat:
            raise serializers.ValidationError('Password do not match')
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        instance = super().create(validated_data)
        return instance


    class Meta:
        model = USER_MODEL
        fields = '__all__'