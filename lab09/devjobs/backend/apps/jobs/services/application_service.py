import uuid

from apps.jobs.models.application import Application
from apps.jobs.models.candidate import Candidate
from apps.jobs.models.offer import Offer
from apps.jobs.models.recruiter import Recruiter
from apps.jobs.schemas.application import ApplicationCreate, ApplicationUpdate
from apps.jobs.services.base import get_or_raise


class ApplicationService:
  def get_all_by_recruiter(
    self, recruiter_bd: Recruiter, offer_id: uuid.UUID
  ) -> list[Application]:
    offer = get_or_raise(Offer, offer_id)
    if offer.recruiter_id != recruiter_bd.id:  # type: ignore
      raise ValueError('No tienes permiso para ver estas aplicaciones')
    # Traemos los user de los candidates de una vez con join
    return list(
      Application.objects.filter(offer_id=offer_id).select_related(
        'candidate__user'
      )
    )

  def get_all_by_candidate(self, candidate_bd: Candidate) -> list[Application]:
    # Traemos el user de recruiter, location y la company el recruiter además prefetch para technologies
    return list(
      Application.objects.filter(candidate=candidate_bd)
      .select_related(
        'offer__recruiter__user', 'offer__recruiter__company', 'offer__location'
      )
      .prefetch_related('offer__technologies')
    )

  def create(
    self, candidate_bd: Candidate, application: ApplicationCreate
  ) -> Application:
    offer = get_or_raise(Offer, application.offer_id)
    if not offer.status:
      raise ValueError('La oferta de empleo no está activa')

    if Application.objects.filter(
      candidate_id=candidate_bd.id, offer_id=application.offer_id
    ).exists():
      raise ValueError('Ya te has postulado a esta oferta')

    application_bd = Application.objects.create(
      offer_id=application.offer_id,
      candidate_id=candidate_bd.id,
      creator_id=candidate_bd.user_id,  # type: ignore
      modifier_id=candidate_bd.user_id,  # type: ignore
    )
    # Traemos el user de recruiter, location y la company el recruiter además prefetch para technologies
    return (
      Application.objects.select_related(
        'offer__recruiter__user', 'offer__recruiter__company', 'offer__location'
      )
      .prefetch_related('offer__technologies')
      .get(id=application_bd.id)
    )

  def patch(
    self, recruiter_bd: Recruiter, id: uuid.UUID, application: ApplicationUpdate
  ) -> Application:
    application_bd = get_or_raise(Application, id)
    offer = get_or_raise(Offer, application_bd.offer_id)  # type: ignore
    if offer.recruiter_id != recruiter_bd.id:  # type: ignore
      raise ValueError('No tienes permiso para modificar estas aplicaciones')

    application_data = application.model_dump(exclude_unset=True)
    if not application_data:
      return application_bd
    for field, value in application_data.items():
      setattr(application_bd, field, value)
    application_bd.modifier_id = recruiter_bd.user_id  # type: ignore
    application_bd.save()
    application_bd.refresh_from_db()  # type: ignore
    return application_bd


application_service = ApplicationService()
