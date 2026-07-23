import uuid

from django.db import models


class OfferTechnology(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  offer = models.ForeignKey('Offer', on_delete=models.PROTECT, related_name='+')
  technology = models.ForeignKey(
    'Technology', on_delete=models.PROTECT, related_name='+'
  )

  class Meta:
    db_table = 'offers_technologies'
