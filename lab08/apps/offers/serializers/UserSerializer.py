from rest_framework import serializers

from ..models.User import User


class UserChangePasswordSerializer(serializers.Serializer[User]):
  current_password = serializers.CharField(write_only=True)
  new_password = serializers.CharField(write_only=True)


class UserCreateSerializer(serializers.ModelSerializer[User]):
  class Meta:
    model = User
    fields = [
      'username',
      'first_name',
      'last_name',
      'email',
      'password',
    ]
    extra_kwargs = {'password': {'write_only': True}}


class UserResponseSerializer(serializers.ModelSerializer[User]):
  class Meta:
    model = User
    fields = [
      'username',
      'first_name',
      'last_name',
      'email',
    ]


class UserPublicResponseSerializer(serializers.ModelSerializer[User]):
  class Meta:
    model = User
    fields = [
      'first_name',
      'last_name',
      'email',
    ]


class UserUpdateSerializer(serializers.ModelSerializer[User]):
  class Meta:
    model = User
    fields = [
      'first_name',
      'last_name',
      'email',
    ]
