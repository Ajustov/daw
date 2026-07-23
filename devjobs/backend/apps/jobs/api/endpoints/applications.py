import uuid

from apps.jobs.api.permissions import CandidateAuth, RecruiterAuth
from apps.jobs.schemas.application import (
  ApplicationCreate,
  ApplicationResponseCandidate,
  ApplicationResponseRecruiter,
  ApplicationUpdate,
)
from apps.jobs.services.application_service import application_service
from ninja import Router
from ninja.errors import HttpError

router_applications = Router(tags=['Applications'])


@router_applications.get(
  '/me', auth=CandidateAuth(), response=list[ApplicationResponseCandidate]
)
def get_all_by_candidate(request):
  return application_service.get_all_by_candidate(request.auth)


@router_applications.post(
  '', auth=CandidateAuth(), response={201: ApplicationResponseCandidate}
)
def post(request, application: ApplicationCreate):
  try:
    return application_service.create(request.auth, application)
  except ValueError as e:
    raise HttpError(400, str(e))


@router_applications.patch(
  '/{id}', auth=RecruiterAuth(), response=ApplicationResponseRecruiter
)
def patch(request, id: uuid.UUID, application: ApplicationUpdate):
  try:
    return application_service.patch(request.auth, id, application)
  except PermissionError as e:
    raise HttpError(403, str(e))
  except ValueError as e:
    raise HttpError(400, str(e))
