import uuid

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class Recruiter(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL, on_delete=models.PROTECT
  )
  company = models.ForeignKey(
    'Company', on_delete=models.PROTECT, related_name='+'
  )
  description = models.CharField(
    null=True, validators=[MinLengthValidator(2)], max_length=500
  )
  contact_email = models.EmailField()
  status = models.BooleanField(default=True)
  created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='+',
  )
  modified = models.DateTimeField(auto_now=True)
  modifier = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='+',
  )

  class Meta:
    db_table = 'recruiters'

  def __str__(self):
    return f'{self.user.get_full_name()} - {self.company.name}'
