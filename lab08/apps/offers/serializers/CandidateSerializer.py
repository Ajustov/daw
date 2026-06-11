from ..models.Candidate import Candidate
from .UserSerializer import (
  UserCreateSerializer,
  UserPublicResponseSerializer,
  UserResponseSerializer,
  UserUpdateSerializer,
)


class CandidateCreateSerializer(UserCreateSerializer):
  class Meta(UserCreateSerializer.Meta):
    model = Candidate
    fields = UserCreateSerializer.Meta.fields + [
      'description',
      'cv',
      'seniority',
      'experienceYears',
    ]


class CandidateResponseSerializer(UserResponseSerializer):
  class Meta(UserResponseSerializer.Meta):
    model = Candidate
    fields = UserResponseSerializer.Meta.fields + [
      'id',
      'description',
      'cv',
      'seniority',
      'experienceYears',
    ]


class CandidatePublicResponseSerializer(UserPublicResponseSerializer):
  class Meta(UserPublicResponseSerializer.Meta):
    model = Candidate
    fields = UserPublicResponseSerializer.Meta.fields + [
      'id',
      'description',
      'seniority',
      'experienceYears',
    ]


class CandidateUpdateSerializer(UserUpdateSerializer):
  class Meta(UserUpdateSerializer.Meta):
    model = Candidate
    fields = UserUpdateSerializer.Meta.fields + [
      'description',
      'cv',
      'seniority',
      'experienceYears',
    ]
