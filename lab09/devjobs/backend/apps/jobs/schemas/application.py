import uuid
from datetime import datetime

from apps.jobs.models.application import Status
from apps.jobs.schemas.candidate import CandidateResponsePublic
from apps.jobs.schemas.offer import OfferResponseSummary
from pydantic import BaseModel, field_validator


class ApplicationCreate(BaseModel):
  offer_id: uuid.UUID


class ApplicationResponse(BaseModel):
  id: uuid.UUID
  offer_id: uuid.UUID
  candidate_id: uuid.UUID
  status: Status
  created: datetime
  modified: datetime


class ApplicationResponseRecruiter(BaseModel):
  model_config = {'from_attributes': True}
  id: uuid.UUID
  candidate: CandidateResponsePublic
  status: Status
  created: datetime
  modified: datetime


class ApplicationResponseCandidate(BaseModel):
  model_config = {'from_attributes': True}
  id: uuid.UUID
  offer: OfferResponseSummary
  status: Status
  created: datetime
  modified: datetime


class ApplicationUpdate(BaseModel):
  status: Status | None = None

  @field_validator('status')
  def validate_status(cls, v: Status | None) -> Status:
    if v is None:
      raise ValueError('status no puede ser null')
    return v
