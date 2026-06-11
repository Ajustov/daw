import uuid

from apps.offers.models.validators import validate_description_length
from devjobs import settings
from django.db import models


class Recruiter(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user_id = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    unique=True,
    db_column='user_id',
  )
  company_id = models.ForeignKey('Company', on_delete=models.PROTECT)
  description = models.TextField(
    null=True, validators=[validate_description_length]
  )
  status = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  created_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    on_delete=models.PROTECT,
    related_name='+',
    db_column='created_id',
  )
  modified = models.DateTimeField(auto_now=True)
  modified_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    on_delete=models.PROTECT,
    related_name='+',
    db_column='modified_id',
  )

  class Meta:
    db_table = 'recruiters'

  def __str__(self):
    return f'{self.user_id.get_full_name()} - {self.company_id.name}'
