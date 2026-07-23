import uuid

from apps.jobs.models.enums import Seniority
from django.conf import settings
from django.core.validators import (
  MaxValueValidator,
  MinValueValidator,
)
from django.db import models


class Candidate(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL, on_delete=models.PROTECT
  )
  description = models.CharField(null=True, max_length=500)
  seniority = models.CharField(
    max_length=7,  # Me obliga max_length aunque sea un enum
    choices=Seniority.choices,
  )
  experience_years = models.IntegerField(
    validators=[MinValueValidator(0), MaxValueValidator(50)]
  )
  status = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='+',
  )
  modified = models.DateTimeField(auto_now=True)
  modifier = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='+',
  )

  class Meta:
    db_table = 'candidates'

  def __str__(self):
    return f'{self.user.get_full_name()} - {self.seniority}'
