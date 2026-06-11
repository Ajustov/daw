from django.db import models


class OfferTechnology(models.Model):
  offer_id = models.ForeignKey('Offer', on_delete=models.PROTECT)
  technology_id = models.ForeignKey('Technology', on_delete=models.PROTECT)

  class Meta:
    db_table = 'offers_technologies'
