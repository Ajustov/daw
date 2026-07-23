import uuid

from apps.jobs.schemas.company import CompanyResponseSummary
from apps.jobs.schemas.user import UserResponseRecruiter
from ninja import Field
from pydantic import BaseModel, EmailStr, field_validator


class RecruiterCreate(BaseModel):
  company_id: uuid.UUID
  contact_email: EmailStr
  description: str | None = Field(default=None, max_length=500)

  @field_validator('description')
  def validate_description(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == '':
        return None
    return v


class RecruiterResponsePrivate(BaseModel):
  model_config = {'from_attributes': True}
  id: uuid.UUID
  company_id: uuid.UUID
  contact_email: EmailStr
  description: str | None


class RecruiterResponseSummary(BaseModel):
  model_config = {'from_attributes': True}
  company: CompanyResponseSummary


class RecruiterResponseApplication(RecruiterResponseSummary):
  user: UserResponseRecruiter


class RecruiterResponsePublic(RecruiterResponseSummary):
  id: uuid.UUID
  user: UserResponseRecruiter
  contact_email: EmailStr


class RecruiterUpdate(BaseModel):
  company_id: uuid.UUID | None = None
  contact_email: EmailStr | None = None
  description: str | None = Field(default=None, max_length=500)
  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente

  @field_validator('company_id')
  def validate_company_id(cls, v: uuid.UUID | None) -> uuid.UUID:
    if v is None:
      raise ValueError('company_id no puede ser null')
    return v

  @field_validator('contact_email')
  def validate_contact_email(cls, v: EmailStr | None) -> EmailStr:
    if v is None:
      raise ValueError('EmailStr no puede ser null')
    return v

  @field_validator('description')
  def validate_description(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == '':
        return None
    return v
