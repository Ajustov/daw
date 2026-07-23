import uuid
from datetime import datetime
from decimal import Decimal

from apps.jobs.models.enums import Seniority
from apps.jobs.models.offer import Modality
from apps.jobs.schemas.location import LocationResponseDetail, LocationResponseSummary
from apps.jobs.schemas.recruiter import (
  RecruiterResponseApplication,
  RecruiterResponsePublic,
  RecruiterResponseSummary,
)
from apps.jobs.schemas.technology import TechnologyResponse
from ninja import Field, Schema
from pydantic import BaseModel, field_validator


class OfferCreate(BaseModel):
  title: str = Field(min_length=3, max_length=255)
  description_detail: str = Field(min_length=10, max_length=2000)
  location_id: uuid.UUID
  modality: Modality
  seniority: Seniority
  technologies_ids: list[uuid.UUID]
  salary: Decimal | None = Field(
    default=None, ge=0, decimal_places=2, max_digits=10
  )

  @field_validator('title')
  def validate_title(cls, v: str) -> str:
    if v.strip() == '':
      raise ValueError('title no puede estar vacío')
    return v.lower()

  @field_validator('description_detail')
  def validate_description_detail(cls, v: str) -> str:
    if v.strip() == '':
      raise ValueError('description_detail no puede estar vacío')
    return v


# Schema porque usamos el resolver de ninja
class OfferResponseSummary(Schema):
  model_config = {'from_attributes': True}
  id: uuid.UUID
  recruiter: RecruiterResponseSummary
  title: str
  description_summary: str
  location: LocationResponseSummary
  modality: Modality
  seniority: Seniority
  salary: Decimal | None
  technologies: list[TechnologyResponse]

  # Para que se ejecute tengo que llamar al all()
  @staticmethod
  def resolve_technologies(obj):
    return obj.technologies.all()


# Schema porque usamos el resolver de ninja
class OfferResponseDetail(Schema):
  model_config = {'from_attributes': True}
  id: uuid.UUID
  recruiter: RecruiterResponsePublic
  title: str
  description_detail: str
  location: LocationResponseDetail
  modality: Modality
  seniority: Seniority
  salary: Decimal | None
  technologies: list[TechnologyResponse]
  created: datetime
  modified: datetime

  # Para que se ejecute tengo que llamar al all()
  @staticmethod
  def resolve_technologies(obj):
    return obj.technologies.all()


# Schema porque usamos el resolver de ninja
class OfferResponseApplication(Schema):
  model_config = {'from_attributes': True}
  id: uuid.UUID
  recruiter: RecruiterResponseApplication
  title: str
  location: LocationResponseSummary
  modality: Modality
  seniority: Seniority
  salary: Decimal | None


class OfferResponseRecruiter(Schema):
  model_config = {'from_attributes': True}
  id: uuid.UUID
  title: str
  location: LocationResponseSummary
  modality: Modality
  seniority: Seniority
  salary: Decimal | None


class OfferUpdate(BaseModel):
  title: str | None = Field(default=None, min_length=3, max_length=255)
  description_detail: str | None = Field(
    default=None, min_length=10, max_length=2000
  )
  location_id: uuid.UUID | None = None
  modality: Modality | None = None
  seniority: Seniority | None = None
  technologies_ids: list[uuid.UUID] | None = None
  salary: Decimal | None = Field(
    default=None, ge=0, decimal_places=2, max_digits=10
  )

  @field_validator('title', 'description_detail')
  def validate_title_description_detail(cls, v: str | None, info) -> str:
    if v is None:
      raise ValueError(f'{info.field_name} no puede ser null')
    return v

  @field_validator('location_id')
  def validate_location_id(cls, v: uuid.UUID | None) -> uuid.UUID:
    if v is None:
      raise ValueError('location_id no puede ser null')
    return v

  @field_validator('modality')
  def validate_modality(cls, v: Modality | None) -> Modality:
    if v is None:
      raise ValueError('modality no puede ser null')
    return v

  @field_validator('seniority')
  def validate_seniority(cls, v: Seniority | None) -> Seniority:
    if v is None:
      raise ValueError('seniority no puede ser null')
    return v

  @field_validator('technologies_ids')
  def validate_technologies(cls, v: list[uuid.UUID] | None) -> list[uuid.UUID]:
    if v is None:
      raise ValueError('technologies_ids no puede ser null')
    return v
