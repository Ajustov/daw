import uuid

from apps.jobs.api.permissions import RecruiterAuth
from apps.jobs.models.offer import Modality
from apps.jobs.schemas.application import ApplicationResponseRecruiter
from apps.jobs.schemas.offer import (
  OfferCreate,
  OfferResponseDetail,
  OfferResponseSummary,
  OfferUpdate,
)
from apps.jobs.services.application_service import application_service
from apps.jobs.services.offer_service import offer_service
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import LimitOffsetPagination, paginate

router_offers = Router(tags=['Offers'])


@router_offers.get('/', response=list[OfferResponseSummary])
@paginate(LimitOffsetPagination)
def get_all(
  request,
  title: str | None = None,
  location_id: uuid.UUID | None = None,
  modality: Modality | None = None,
  technology_id: uuid.UUID | None = None,
):
  return offer_service.get_all(title, location_id, modality, technology_id)


@router_offers.get(
  '/me', auth=RecruiterAuth(), response=list[OfferResponseSummary]
)
@paginate(LimitOffsetPagination)
def get_all_by_recruiter(
  request,
  title: str | None = None,
  location_id: uuid.UUID | None = None,
  modality: Modality | None = None,
  technology_id: uuid.UUID | None = None,
):
  return offer_service.get_all_by_recruiter(
    request.auth, title, location_id, modality, technology_id
  )


@router_offers.get('/{id}', response=OfferResponseDetail)
def get(request, id: uuid.UUID):
  try:
    return offer_service.get(id)
  except ValueError as e:
    raise HttpError(404, str(e))


@router_offers.get(
  '/{id}/applications',
  auth=RecruiterAuth(),
  response=list[ApplicationResponseRecruiter],
)
def get_applications(request, id: uuid.UUID):
  return application_service.get_all_by_recruiter(request.auth, id)


@router_offers.post(
  '/', auth=RecruiterAuth(), response={201: OfferResponseDetail}
)
def post(request, offer: OfferCreate):
  return offer_service.create(request.auth, offer)


@router_offers.patch(
  '/{id}', auth=RecruiterAuth(), response=OfferResponseDetail
)
def patch(request, id: uuid.UUID, offer: OfferUpdate):
  try:
    return offer_service.patch(id, request.auth, offer)
  except ValueError as e:
    raise HttpError(404, str(e))


@router_offers.delete(
  '/{id}', auth=RecruiterAuth(), response=OfferResponseDetail
)
def deactivate(request, id: uuid.UUID):
  try:
    return offer_service.deactivate(id, request.auth)
  except ValueError as e:
    raise HttpError(404, str(e))
