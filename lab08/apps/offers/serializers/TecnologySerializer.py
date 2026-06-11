from rest_framework import serializers

from ..models.Technology import Technology


class TechnologyCreateSerializer(serializers.ModelSerializer[Technology]):
  class Meta:
    model = Technology
    fields = ['name']


class TechnologyResponseSerializer(serializers.ModelSerializer[Technology]):
  class Meta:
    model = Technology
    fields = ['id', 'name']
    read_only_fields = ['id', 'name']


class TechnologyUpdateSerializer(serializers.ModelSerializer[Technology]):
  class Meta:
    model = Technology
    fields = ['name']
