import uuid
from typing import TypeVar

from django.db import models

T = TypeVar('T', bound=models.Model)


def get_or_raise(model: type[T], id: uuid.UUID) -> T:
  try:
    return model.objects.get(id=id)
  except model.DoesNotExist:
    raise ValueError(f'{model.__name__} not found')
