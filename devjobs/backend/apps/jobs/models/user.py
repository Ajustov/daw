import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
  # Los atributos que ya vienen por defecto
  # username
  first_name = models.CharField(_('first name'), max_length=150, blank=True)
  last_name = models.CharField(_('last name'), max_length=150, blank=True)
  # email
  # password
  # is_active
  # is_staff, si puede acceder al ADMIN
  # is_superuser
  # last_login
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  # status, no está porque lo reemplaza is_active
  # date_joined, es lo mismo que created
  creator = models.ForeignKey(
    'self', null=True, on_delete=models.PROTECT, blank=True, related_name='+'
  )
  modified = models.DateTimeField(auto_now=True)
  modifier = models.ForeignKey(
    'self', null=True, on_delete=models.PROTECT, blank=True, related_name='+'
  )

  # Heredamos su __str__
  class Meta:
    db_table = 'users'
    indexes = [
      models.Index(
        fields=['first_name', 'last_name'], name='idx_user_full_name'
      )
    ]

  def save(self, *args, **kwargs) -> None:
    if self.first_name:
      self.first_name = self.first_name.strip().upper()
    if self.last_name:
      self.last_name = self.last_name.strip().upper()
    super().save(*args, **kwargs)
