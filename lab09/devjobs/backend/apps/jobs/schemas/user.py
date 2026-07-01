from datetime import datetime

from ninja import Field
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
  username: str = Field(min_length=3, max_length=150)
  first_name: str | None = Field(default=None, min_length=2, max_length=150)
  last_name: str | None = Field(default=None, min_length=2, max_length=150)
  email: EmailStr
  password: str

  @field_validator('username')
  def validate_username(cls, v: str) -> str:
    if v.strip() == '':
      raise ValueError('username no puede estar vacío')
    return v.lower()

  @field_validator('first_name', 'last_name')
  def validate_first_name_last_name(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == '':
        return None
      return v.lower()
    return v


class UserResponsePrivate(BaseModel):
  model_config = {'from_attributes': True}
  username: str
  first_name: str
  last_name: str
  email: str
  date_joined: datetime


class UserResponseRecruiter(BaseModel):
  model_config = {'from_attributes': True}
  first_name: str


class UserResponseCandidate(UserResponseRecruiter):
  first_name: str
  last_name: str


class UserUpdate(BaseModel):
  username: str | None = Field(default=None, min_length=3, max_length=150)
  first_name: str | None = Field(default=None, min_length=2, max_length=150)
  last_name: str | None = Field(default=None, min_length=2, max_length=150)
  email: EmailStr | None = None
  password: str | None = None

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente

  @field_validator('username', 'password')
  def validate_username_password(cls, v: str | None, info) -> str:
    if v is None:
      raise ValueError(f'{info.field_name} no puede ser null')
    return v

  @field_validator('first_name', 'last_name')
  def validate_first_name_last_name(cls, v: str | None) -> str | None:
    if v is not None:
      if v.strip() == '':
        return None
    return v

  @field_validator('email')
  def validate_email(cls, v: EmailStr | None) -> EmailStr:
    if v is None:
      raise ValueError('email no puede ser null')
    return v
