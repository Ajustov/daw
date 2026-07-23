from datetime import datetime

from ninja import Field
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
  username: str = Field(min_length=3, max_length=150)
  first_name: str | None = Field(default=None, min_length=2, max_length=150)
  last_name: str | None = Field(default=None, min_length=2, max_length=150)
  email: EmailStr
  password: str = Field(min_length=8)

  @field_validator('password')
  @classmethod
  def validate_password(cls, value: str) -> str:
    if value.isdigit():
      raise ValueError('La contraseña no puede ser completamente numérica')
    return value

  @field_validator('username')
  def validate_username(cls, v: str) -> str:
    if v.strip() == '':
      raise ValueError('username no puede estar vacío')
    return v

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


class UserResponseMe(UserResponsePrivate):
  date_joined: datetime
  has_candidate: bool
  has_recruiter: bool


class UserResponseRecruiter(BaseModel):
  model_config = {'from_attributes': True}
  first_name: str


class UserResponseCandidate(UserResponseRecruiter):
  last_name: str


class UserUpdatePassword(BaseModel):
  current_password: str = Field(min_length=1)
  new_password: str = Field(min_length=8)

  @field_validator('new_password')
  @classmethod
  def not_entirely_numeric(cls, value: str) -> str:
    if value.isdigit():
      raise ValueError('La contraseña no puede ser completamente numérica')
    return value


class UserUpdate(BaseModel):
  username: str | None = Field(default=None, min_length=3, max_length=150)
  first_name: str | None = Field(default=None, min_length=2, max_length=150)
  last_name: str | None = Field(default=None, min_length=2, max_length=150)
  email: EmailStr | None = None

  # Necesitamos el validator de None por si el usuario manda null y recordemos que los validators solo sirven para campos declarados explicitamente

  @field_validator('username')
  def validate_username_password(cls, v: str | None) -> str:
    if v is None:
      raise ValueError('username no puede ser null')
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
