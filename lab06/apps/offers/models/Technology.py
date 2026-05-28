import uuid
from typing import Iterable

from devjobs import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_technology_name(value: str) -> None:
  if not value.strip():
    raise ValidationError('El nombre no puede estar vacío o ser espacios')


class Technology(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100, unique=True)
  status = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  created_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
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
