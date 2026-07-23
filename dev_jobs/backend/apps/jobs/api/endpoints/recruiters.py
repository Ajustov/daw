from apps.jobs.api.permissions import RecruiterAuth, UserAuth
from apps.jobs.schemas.recruiter import (
  RecruiterCreate,
  RecruiterResponsePrivate,
  RecruiterUpdate,
)
from apps.jobs.services.recruiter_service import recruiter_service
from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError

router_recruiters = Router(tags=['Recruiters'])


@router_recruiters.get(
  '/me', auth=RecruiterAuth(), response=RecruiterResponsePrivate
)
def get_me(request):
  return request.auth


@router_recruiters.post(
  '', auth=UserAuth(), response={201: RecruiterResponsePrivate}
)
def create(request, recruiter: RecruiterCreate):
  try:
    return recruiter_service.create(request.user.id, recruiter)
  except (ValueError, IntegrityError) as e:
    raise HttpError(409, str(e))


@router_recruiters.patch(
  '/me', auth=RecruiterAuth(), response=RecruiterResponsePrivate
)
def patch(request, recruiter: RecruiterUpdate):
  try:
    return recruiter_service.patch(request.auth, recruiter)
  except IntegrityError as e:
    raise HttpError(409, str(e))


@router_recruiters.delete('/me', auth=RecruiterAuth(), response={204: None})
def deactivate(request):
  recruiter_service.deactivate(request.auth)
