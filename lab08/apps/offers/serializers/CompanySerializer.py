from rest_framework import serializers

from ..models.Company import Company


class CompanyCreateSerializer(serializers.ModelSerializer[Company]):
  class Meta:
    model = Company
    fields = ['name']


class CompanyResponseSerializer(serializers.ModelSerializer[Company]):
  class Meta:
    model = Company
    fields = ['id', 'name']
    read_only_fields = ['id', 'name']


class CompanyUpdateSerializer(serializers.ModelSerializer[Company]):
  class Meta:
    model = Company
    fields = ['name']
