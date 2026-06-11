from ..models.Recruiter import Recruiter
from .UserSerializer import (
  UserCreateSerializer,
  UserResponseSerializer,
  UserUpdateSerializer,
)


class RecruiterCreateSerializer(UserCreateSerializer):
  class Meta(UserCreateSerializer.Meta):
    model = Recruiter
    fields = UserCreateSerializer.Meta.fields + [
      'description',
    ]


class RecruiterResponseSerializer(UserResponseSerializer):
  class Meta(UserResponseSerializer.Meta):
    model = Recruiter
    fields = UserResponseSerializer.Meta.fields + [
      'company_id',
      'description',
    ]


class RecruiterUpdateSerializer(UserUpdateSerializer):
  class Meta(UserUpdateSerializer.Meta):
    model = Recruiter
    fields = UserUpdateSerializer.Meta.fields + [
      'description',
    ]
