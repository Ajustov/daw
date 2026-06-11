import uuid

from apps.offers.models.enums import Seniority
from apps.offers.models.validators import (
  validate_cv,
  validate_description_length,
  validate_experience_years,
)
from devjobs import settings
from django.db import models


class Candidate(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user_id = models.OneToOneField(  # type: ignore
    settings.AUTH_USER_MODEL, on_delete=models.PROTECT, unique=True
  )
  description = models.TextField(
    null=True, validators=[validate_description_length]
  )
  cv = models.FileField(upload_to='cv/', null=True, validators=[validate_cv])
  seniority = models.CharField(
    max_length=6,  # Me obliga max_length aunque sea un enum
    choices=Seniority.choices,
  )
  experienceYears = models.IntegerField(validators=[validate_experience_years])
  status = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  created_id = models.ForeignKey(
    'User',
    null=True,
    on_delete=models.PROTECT,
    related_name='+',
  )
  modified = models.DateTimeField(auto_now=True)
  modified_id = models.ForeignKey(
    'User',
    null=True,
    on_delete=models.PROTECT,
    related_name='+',
  )

  class Meta:
    db_table = 'candidates'

  def __str__(self):
    return f'{self.user_id.get_full_name()} - {self.seniority}'  # type: ignore
