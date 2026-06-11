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
  offer_id = models.ForeignKey('Offer', on_delete=models.PROTECT)  # type: ignore
  candidate_id = models.ForeignKey('Candidate', on_delete=models.PROTECT)  # type: ignore
  recruiter_id = models.ForeignKey(
    'Recruiter', null=True, on_delete=models.PROTECT, related_name='+'
  )
  status = models.CharField(
    max_length=8, choices=Status.choices, default=Status.PENDING
  )
  created = models.DateTimeField(auto_now_add=True)
  created_id = models.ForeignKey(  # type: ignore
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='+',
  )
  modified = models.DateTimeField(auto_now=True)
  modified_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    on_delete=models.PROTECT,
    related_name='+',
  )

  class Meta:
    db_table = 'applications'

  def __str__(self) -> str:
    return f'{self.candidate_id} - {self.offer_id} - {self.status}'  # type: ignore
