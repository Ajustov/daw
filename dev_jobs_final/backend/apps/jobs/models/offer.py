import uuid
from collections.abc import Iterable

from apps.jobs.models.enums import Modality, Seniority
from devjobs import settings
from django.core.validators import MinLengthValidator
from django.db import models


class Offer(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  recruiter = models.ForeignKey(
    'Recruiter', on_delete=models.PROTECT, related_name='+'
  )
  title = models.CharField(validators=[MinLengthValidator(3)], max_length=255)
  description_detail = models.CharField(
    validators=[MinLengthValidator(10)], max_length=2000
  )
  location = models.ForeignKey(
    'Location', on_delete=models.PROTECT, related_name='+'
  )
  modality = models.CharField(choices=Modality.choices, max_length=10)
  seniority = models.CharField(choices=Seniority.choices, max_length=7)
  technologies = models.ManyToManyField(
    'Technology', through='OfferTechnology', related_name='offers'
  )
  status = models.BooleanField(default=True)
  salary = models.DecimalField(decimal_places=2, null=True, max_digits=10)
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

  # force_insert, force_update, using, update_filds, parámetros de django
  def save(  # type: ignore[override]
    self,
    force_insert: bool = False,
    force_update: bool = False,
    using: str | None = None,
    update_fields: Iterable[str] | None = None,
  ) -> None:
    self.title = self.title.strip().upper()
    super().save(
      force_insert=force_insert,
      force_update=force_update,
      using=using,
      update_fields=update_fields,
    )

  @property
  def description_summary(self) -> str:
    palabras = self.description_detail.split()
    texto_plano = ' '.join(palabras)
    if len(texto_plano) <= 250:
      return texto_plano
    # rsplit: inicia de atras -> adelante
    # 1: cuantos cortes hago
    return texto_plano[0:250].rsplit(' ', 1)[0]
