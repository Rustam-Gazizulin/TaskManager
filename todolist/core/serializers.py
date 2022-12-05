from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


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

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )
        if not user:
            raise AuthenticationFailed
        return user

    class Meta:
        model = USER_MODEL
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
