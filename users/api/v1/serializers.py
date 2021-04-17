from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, get_password_validators
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from users.models import UserProfile

AUTH_PASSWORD_VALIDATORS = getattr(settings, 'AUTH_PASSWORD_VALIDATORS')

User = get_user_model()


class LoginSerializer(JSONWebTokenSerializer):
    def set_user_as_inactive(self, email):
        user = User.objects.get(email=email)
        user.is_active = False
        user.save()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'type',
        )


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    def get_profile(self, user):
        profile = UserProfile.objects.get(user=user)
        return profile

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'profile',
        )
        read_only_fields = (
            'email',
            'profile',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    type = serializers.IntegerField(default=UserProfile.TYPE_CUSTOMER, write_only=True)

    def validate_password(self, password) -> str:
        password2 = self.context.get('request').data.get('password2')
        if password != password2:
            raise ValidationError('Password mismatch')

        validate_password(password, password_validators=get_password_validators(AUTH_PASSWORD_VALIDATORS))
        return password

    def create(self, validated_data: dict) -> User:
        validated_data.pop('password2')

        type = validated_data.pop('type', '')

        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            type=type,
        )

        return user

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'email',
            'first_name',
            'type',
        )


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate_old_password(self, password):
        user = self.context.get('request').user

        if not user.check_password(password):
            raise ValidationError('Wrong old password')

        return password

    def validate_new_password(self, password):
        old_password = self.context.get('request').data.get('old_password')

        if password == old_password:
            raise ValidationError('Password can\'t be the same as the old one')

        password2 = self.context.get('request').data.get('new_password2')
        if password != password2:
            raise ValidationError('Password mismatch')

        validate_password(password, password_validators=get_password_validators(AUTH_PASSWORD_VALIDATORS))

        return password

    def save(self, *args, **kwargs):
        new_password = self.validated_data.get('new_password')
        self.instance.set_password(new_password)
        self.instance.save()

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2', )
