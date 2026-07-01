import uuid

from apps.jobs.models.recruiter import Recruiter
from apps.jobs.schemas.recruiter import (
  RecruiterCreate,
  RecruiterUpdate,
)
from django.db import transaction


class RecruiterService:
  # Para que al fallar, haga rollback de todo
  @transaction.atomic
  def create(self, user_id: uuid.UUID, recruiter: RecruiterCreate) -> Recruiter:
    if Recruiter.objects.filter(user_id=user_id).exists():
      raise ValueError('El usuario ya tiene un perfil de reclutador')
    return Recruiter.objects.create(
      user_id=user_id,
      creator_id=user_id,
      modifier_id=user_id,
      **recruiter.model_dump(),
    )

  @transaction.atomic
  def patch(
    self, recruiter_bd: Recruiter, recruiter: RecruiterUpdate
  ) -> Recruiter:
    recruiter_data = recruiter.model_dump(exclude_unset=True)
    if not recruiter_data:
      return recruiter_bd
    for field, value in recruiter_data.items():
      setattr(recruiter_bd, field, value)
    recruiter_bd.modifier_id = recruiter_bd.user_id  # type: ignore
    recruiter_bd.save()
    return recruiter_bd

  @transaction.atomic
  def deactivate(self, recruiter_bd: Recruiter) -> Recruiter:
    recruiter_bd.status = False
    recruiter_bd.modifier_id = recruiter_bd.user_id  # type: ignore
    recruiter_bd.save()
    return recruiter_bd


recruiter_service = RecruiterService()
