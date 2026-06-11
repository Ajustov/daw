from rest_framework import serializers

from ..models.Offer import Offer


class OfferCreateSerializer(serializers.ModelSerializer[Offer]):
  class Meta:
    model = Offer
    fields = [
      'title',
      'description',
      'location',
      'modality',
      'seniority',
      'salary',
    ]


class OfferResponseSerializer(serializers.ModelSerializer[Offer]):
  class Meta:
    model = Offer
    fields = [
      'id',
      'title',
      'description',
      'location',
      'modality',
      'seniority',
      'salary',
      'status',
    ]
    read_only_fields = [
      'id',
      'title',
      'description',
      'location',
      'modality',
      'seniority',
      'salary',
      'status',
    ]


class OfferUpdateSerializer(serializers.ModelSerializer[Offer]):
  class Meta:
    model = Offer
    fields = [
      'title',
      'description',
      'location',
      'modality',
      'seniority',
      'salary',
    ]
