from apps.offers.models import Candidate
from rest_framework import serializers


class CandidateCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Candidate

    fields = ['description', 'cv', 'seniority', 'experienceYears']


class CandidateResponseSerializer(serializers.ModelSerializer):
  class Meta:
    model = Candidate

    fields = ['id', 'description', 'cv', 'seniority', 'experienceYears']

    read_only_fields = [
      'id',
      'description',
      'cv',
      'seniority',
      'experienceYears',
    ]


class CandidateUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Candidate

    fields = ['description', 'cv', 'seniority', 'experienceYears']
