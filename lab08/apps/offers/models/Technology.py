import uuid
from typing import Iterable

from apps.offers.models.validators import validate_technology_name
from devjobs import settings
from django.db import models


class Technology(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(
    max_length=100, unique=True, validators=[validate_technology_name]
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
    db_table = 'technologies'

  def __str__(self):
    return f'{self.name}'

  def save(
    self,
    force_insert: bool = False,
    force_update: bool = False,
    using: str | None = None,
    update_fields: Iterable[str] | None = None,
  ) -> None:
    self.name = self.name.strip().upper()
    super().save(force_insert, force_update, using, update_fields)
