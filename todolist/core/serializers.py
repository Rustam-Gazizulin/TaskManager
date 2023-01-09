from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        instance = USER_MODEL.objects.create_user(**validated_data)
        return instance

    class Meta:
        model = USER_MODEL
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password_repeat'
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('password or username is not correct')
        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = attrs['user']
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('Прежний пароль введен неверно.')
        try:
            validate_password(attrs['new_password'])
        except Exception as e:
            raise serializers.ValidationError({'new_password': e.messages})
        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
