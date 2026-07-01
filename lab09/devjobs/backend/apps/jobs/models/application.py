import uuid

from devjobs import settings
from django.db import models


class Status(models.TextChoices):
  PENDING = 'pending'
  REVIEWED = 'reviewed'
  REJECTED = 'rejected'
  HIRED = 'hired'


class Application(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  offer = models.ForeignKey('Offer', on_delete=models.PROTECT, related_name='+')
  candidate = models.ForeignKey(
    'Candidate', on_delete=models.PROTECT, related_name='+'
  )
  status = models.CharField(
    max_length=8, choices=Status.choices, default=Status.PENDING
  )
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
    db_table = 'applications'

  def __str__(self) -> str:
    return f'{self.candidate} - {self.offer} - {self.status}'
