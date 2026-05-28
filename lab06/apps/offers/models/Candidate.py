import uuid

from apps.offers.models.enums import Seniority
from devjobs import settings
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models


def validate_cv(value: File) -> None:
  if not value.name.endswith('.pdf'):
    raise ValidationError('Solo se permiten archivos PDF')
  if value.size > 5 * 1024 * 1024:
    raise ValidationError('El archivo no puede superar 5MB')


def validate_experience_years(value: int) -> None:
  if value < 0:
    raise ValidationError('La experiencia no puede ser negativa')
  if value > 50:
    raise ValidationError('La experiencia no es realista')


def validate_description_length(value: str) -> None:
  if len(value) > 500:
    raise ValidationError('La descripción no puede superar 500 caracteres')


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
