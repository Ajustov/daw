import uuid
from typing import Iterable

from apps.offers.models.enums import Seniority
from devjobs import settings
from django.db import models


class Modality(models.TextChoices):
  REMOTE = 'remote'
  PRESENTIAL = 'presential'
  HYBRID = 'hybrid'


class Offer(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  recruiter = models.ForeignKey(
    'Recruiter', on_delete=models.PROTECT, related_name='+'
  )
  title = models.CharField(max_length=255)
  description = models.TextField()
  location = models.CharField(max_length=255)
  modality = models.CharField(max_length=10, choices=Modality.choices)
  seniority = models.CharField(max_length=6, choices=Seniority.choices)
  status = models.BooleanField(default=True)
  salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
  created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+'
  )
  modified = models.DateTimeField(auto_now=True)
  modifier = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    on_delete=models.PROTECT,
    related_name='+',
  )

  class Meta:
    db_table = 'offers'

  def __str__(self) -> str:
    return f'{self.title} - {self.location}'

  def save(
    self,
    force_insert: bool = False,
    force_update: bool = False,
    using: str | None = None,
    update_fields: Iterable[str] | None = None,
  ) -> None:
    self.title = self.title.strip().upper()
    self.location = self.location.strip().upper()
    super().save(force_insert, force_update, using, update_fields)
