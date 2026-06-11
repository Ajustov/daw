from django.core.exceptions import ValidationError
from django.core.files import File


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


def validate_technology_name(value: str) -> None:
  if not value.strip():
    raise ValidationError('El nombre no puede estar vacío o ser espacios')
