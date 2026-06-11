from rest_framework import serializers

from ..models.Application import Application


class ApplicationCreateSerializer(serializers.ModelSerializer[Application]):
  class Meta:
    model = Application
    fields = ['offer_id']


class ApplicationResponseSerializer(serializers.ModelSerializer[Application]):
  class Meta:
    model = Application
    fields = ['id', 'offer_id', 'candidate_id', 'status']
    read_only_fields = ['id', 'offer_id', 'candidate_id', 'status']


class ApplicationUpdateSerializer(serializers.ModelSerializer[Application]):
  class Meta:
    model = Application
    fields = ['status']
