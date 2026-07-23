import uuid

from apps.jobs.models.candidate import Candidate
from apps.jobs.schemas.candidate import (
  CandidateCreate,
  CandidateUpdate,
)
from django.db import transaction


class CandidateService:
  # Para que al fallar, haga rollback de todo

  @transaction.atomic
  def create(self, user_id: uuid.UUID, candidate: CandidateCreate) -> Candidate:
    if Candidate.objects.filter(user_id=user_id).exists():
      raise ValueError('El usuario ya tiene un perfil de candidato')
    return Candidate.objects.create(
      user_id=user_id,
      creator_id=user_id,
      modifier_id=user_id,
      **candidate.model_dump(),
    )

  @transaction.atomic
  def patch(
    self, candidate_bd: Candidate, candidate: CandidateUpdate
  ) -> Candidate:
    candidate_data = candidate.model_dump(exclude_unset=True)
    if not candidate_data:
      return candidate_bd
    for field, value in candidate_data.items():
      setattr(candidate_bd, field, value)
    candidate_bd.modifier_id = candidate_bd.user_id  # type: ignore
    candidate_bd.save()
    return candidate_bd

  @transaction.atomic
  def deactivate(self, candidate_bd: Candidate) -> None:
    candidate_bd.status = False
    candidate_bd.modifier_id = candidate_bd.user_id  # type: ignore
    candidate_bd.save()


candidate_service = CandidateService()
