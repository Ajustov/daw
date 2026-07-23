from apps.jobs.models.enums import Seniority
from apps.jobs.schemas.user import UserResponseCandidate
from ninja import Field
from pydantic import BaseModel, field_validator


class CandidateCreate(BaseModel):
  description: str | None = Field(default=None, max_length=500)
  seniority: Seniority
  experience_years: int = Field(ge=0, le=50)

  @field_validator('description')
  def validate_description(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == '':
        return None
    return v


class CandidateResponsePrivate(BaseModel):
  model_config = {'from_attributes': True}
  description: str | None
  seniority: Seniority
  experience_years: int


class CandidateResponsePublic(BaseModel):
  model_config = {'from_attributes': True}
  user: UserResponseCandidate
  description: str | None
  seniority: Seniority
  experience_years: int


class CandidateUpdate(BaseModel):
  description: str | None = Field(default=None, max_length=500)
  seniority: Seniority | None = None
  experience_years: int | None = Field(default=None, ge=0, le=50)

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente

  @field_validator('description')
  def validate_description(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == '':
        return None
    return v

  @field_validator('seniority')
  def validate_seniority(cls, v: Seniority | None) -> Seniority:
    if v is None:
      raise ValueError('seniority no puede ser null')
    return v

  @field_validator('experience_years')
  def validate_experience_years(cls, v: Seniority | None) -> Seniority:
    if v is None:
      raise ValueError('experience_years no puede ser null')
    return v
