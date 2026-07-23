from apps.jobs.api.permissions import CandidateAuth, UserAuth
from apps.jobs.schemas.candidate import (
  CandidateCreate,
  CandidateResponsePrivate,
  CandidateUpdate,
)
from apps.jobs.services.candidate_service import candidate_service
from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError

router_candidates = Router(tags=['Candidates'])


@router_candidates.get(
  '/me', auth=CandidateAuth(), response=CandidateResponsePrivate
)
def get_me(request):
  return request.auth


@router_candidates.post(
  '', auth=UserAuth(), response={201: CandidateResponsePrivate}
)
def create(request, candidate: CandidateCreate):
  try:
    return candidate_service.create(request.user.id, candidate)
  except (ValueError, IntegrityError) as e:
    raise HttpError(409, str(e))


@router_candidates.patch(
  '/me', auth=CandidateAuth(), response=CandidateResponsePrivate
)
def patch(request, candidate: CandidateUpdate):
  try:
    return candidate_service.patch(request.auth, candidate)
  except IntegrityError as e:
    raise HttpError(409, str(e))


@router_candidates.delete('/me', auth=CandidateAuth(), response={204: None})
def deactivate(request):
  candidate_service.deactivate(request.auth)
