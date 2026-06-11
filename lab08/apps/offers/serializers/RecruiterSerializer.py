from rest_framework import serializers

from ..models.Recruiter import Recruiter


class RecruiterCreateSerializer(serializers.ModelSerializer[Recruiter]):
  class Meta:
    model = Recruiter

    fields = ['description']


class RecruiterResponseSerializer(serializers.ModelSerializer[Recruiter]):
  class Meta:
    model = Recruiter

    fields = ['id', 'company_id', 'description']

    read_only_fields = ['id', 'company_id', 'description']


class RecruiterUpdateSerializer(serializers.ModelSerializer[Recruiter]):
  class Meta:
    model = Recruiter

    fields = ['description']
