import uuid
from collections.abc import Iterable

from devjobs import settings
from django.core.validators import MinLengthValidator
from django.db import models


class Company(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(validators=[MinLengthValidator(2)], max_length=255)
  status = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    on_delete=models.PROTECT,
    related_name='+',
  )
  modified = models.DateTimeField(auto_now=True)
  modifier = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    on_delete=models.PROTECT,
    related_name='+',
  )

  class Meta:
    db_table = 'companies'

  def __str__(self):
    return f'{self.name}'

  # force_insert, force_update, using, update_filds, parámetros de django
  def save(  # type: ignore[override]
    self,
    force_insert: bool = False,
    force_update: bool = False,
    using: str | None = None,
    update_fields: Iterable[str] | None = None,
  ) -> None:
    self.name = self.name.strip().upper()
    super().save(
      force_insert=force_insert,
      force_update=force_update,
      using=using,
      update_fields=update_fields,
    )
