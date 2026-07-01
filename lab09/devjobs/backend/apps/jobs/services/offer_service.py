import uuid

from apps.jobs.models.offer import Modality, Offer
from apps.jobs.models.recruiter import Recruiter
from apps.jobs.schemas.offer import OfferCreate, OfferUpdate
from apps.jobs.services.base import get_or_raise
from django.db.models import QuerySet


class OfferService:
  # Lazy porque tengo que filtrar y la query es dinámica
  def get_all(
    self,
    title: str | None,
    location_id: uuid.UUID | None,
    modality: Modality | None,
    technology_id: uuid.UUID | None,
  ) -> QuerySet[Offer]:
    # Prefetch porque traigo antes las technologies y no solo los ids para que django no busque uno por uno (N + 1)
    query = Offer.objects.filter(status=True).prefetch_related('technologies')
    if title:
      query = query.filter(title__icontains=title)
    if location_id:
      query = query.filter(location_id=location_id)
    if modality:
      query = query.filter(modality=modality)
    if technology_id:
      query = query.filter(technologies__id=technology_id)
    return query

  def get_all_by_recruiter(
    self,
    recruiter_bd: Recruiter,
    title: str | None,
    location_id: uuid.UUID | None,
    modality: Modality | None,
    technology_id: uuid.UUID | None,
  ) -> QuerySet[Offer]:
    query = Offer.objects.filter(
      status=True, recruiter=recruiter_bd
    ).prefetch_related('technologies')
    if title:
      query = query.filter(title__icontains=title)
    if location_id:
      query = query.filter(location_id=location_id)
    if modality:
      query = query.filter(modality=modality)
    if technology_id:
      query = query.filter(technologies__id=technology_id)
    return query

  def get(self, id: uuid.UUID) -> Offer:
    offer = (
      Offer.objects.prefetch_related('technologies')
      .filter(id=id, status=True)
      .first()
    )
    if offer is None:
      raise ValueError('Offer not found')
    return offer

  def create(self, recruiter_bd: Recruiter, offer: OfferCreate) -> Offer:
    offer_bd = Offer.objects.create(
      creator_id=recruiter_bd.user_id,  # type: ignore
      modifier_id=recruiter_bd.user_id,  # type: ignore
      recruiter_id=recruiter_bd.id,
      **offer.model_dump(exclude={'technologies_ids'}),
    )
    # Obligatorio para relaciones N:M
    offer_bd.technologies.set(offer.technologies_ids)
    return offer_bd

  def patch(
    self, id: uuid.UUID, recruiter_bd: Recruiter, offer: OfferUpdate
  ) -> Offer:
    offer_bd = get_or_raise(Offer, id)
    offer_data = offer.model_dump(
      exclude_unset=True, exclude={'technologies_ids'}
    )
    if offer_data:
      for field, value in offer_data.items():
        setattr(offer_bd, field, value)
      offer_bd.modifier_id = recruiter_bd.user_id  # type: ignore
      offer_bd.save()
    if offer.technologies_ids is not None:
      offer_bd.technologies.set(offer.technologies_ids)
    offer_bd.refresh_from_db()  # type: ignore
    return offer_bd

  def deactivate(self, id: uuid.UUID, recruiter_bd: Recruiter) -> Offer:
    offer_bd = get_or_raise(Offer, id)
    offer_bd.status = False
    offer_bd.modifier_id = recruiter_bd.user_id  # type: ignore
    offer_bd.save()
    return offer_bd


offer_service = OfferService()
