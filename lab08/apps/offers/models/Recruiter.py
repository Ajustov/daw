import uuid

from apps.offers.models.validators import validate_description_length
from devjobs import settings
from django.db import models


class Recruiter(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL, on_delete=models.PROTECT, unique=True, related_name='recruiter_profile'
  )
  company = models.ForeignKey('Company', on_delete=models.PROTECT, related_name='recruiters')
  description = models.TextField(
    null=True, validators=[validate_description_length]
  )
  status = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  created_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    blank=True,  # <-- AGREGAR
    on_delete=models.PROTECT,
    related_name='+',
  )
  modified = models.DateTimeField(auto_now=True)
  modified_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    blank=True,  # <-- AGREGAR
    on_delete=models.PROTECT,
    related_name='+',
  )

  class Meta:
    db_table = 'recruiters'

  def __str__(self):
    return f'{self.user.get_full_name()} - {self.company.name}'  # type: ignore