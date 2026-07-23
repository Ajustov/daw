from apps.jobs.models.candidate import Candidate
from apps.jobs.models.recruiter import Recruiter
from apps.jobs.models.user import User
from apps.jobs.schemas.user import (
  UserCreate,
  UserResponseMe,
  UserResponsePrivate,
  UserUpdate,
  UserUpdatePassword,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from ninja_jwt.token_blacklist.models import BlacklistedToken, OutstandingToken


class UserService:
  def get_me(self, user: User) -> UserResponseMe:
    has_candidate = Candidate.objects.filter(
      user_id=user.id, status=True
    ).exists()
    has_recruiter = Recruiter.objects.filter(
      user_id=user.id, status=True
    ).exists()
    return UserResponseMe(
      **UserResponsePrivate.model_validate(user).model_dump(),
      date_joined=user.date_joined,
      has_candidate=has_candidate,
      has_recruiter=has_recruiter,
    )

  def create(self, user: UserCreate) -> User:
    try:
      validate_password(user.password)
    except ValidationError as e:
      raise ValueError(', '.join(e.messages))
    new_user = User.objects.create_user(
      # Excluimos el password para que django lo hashee
      **user.model_dump(exclude={'password'}),
      password=user.password,
    )
    new_user.creator_id = new_user.id  # type: ignore
    new_user.modifier_id = new_user.id  # type: ignore
    new_user.save()
    return new_user

  def patch_password(self, user_bd: User, data: UserUpdatePassword) -> None:
    if not user_bd.check_password(data.current_password):
      raise ValueError('La contraseña actual es incorrecta')
    if user_bd.check_password(data.new_password):
      raise ValueError('La nueva contraseña no puede ser igual a la actual')
    try:
      validate_password(data.new_password)
    except ValidationError as e:
      raise ValueError(', '.join(e.messages))

    user_bd.set_password(data.new_password)
    user_bd.modifier_id = user_bd.id  # type: ignore
    user_bd.save()

    # Invalido todos sus refresh
    tokens = OutstandingToken.objects.filter(user_id=user_bd.id)
    for token in tokens:
      BlacklistedToken.objects.get_or_create(token=token)

  def patch(self, user_bd: User, user: UserUpdate) -> User:
    user_data = user.model_dump(exclude_unset=True)
    if not user_data:
      return user_bd
    for field, value in user_data.items():
      setattr(user_bd, field, value)
    user_bd.modifier_id = user_bd.id  # type: ignore
    user_bd.save()
    return user_bd

  @transaction.atomic
  def deactivate(self, user_bd: User):
    user_bd.is_active = False
    user_bd.modifier_id = user_bd.id  # type: ignore
    user_bd.save()
    Candidate.objects.filter(user_id=user_bd.id).update(status=False)
    Recruiter.objects.filter(user_id=user_bd.id).update(status=False)

    # Invalido todos sus refresh
    tokens = OutstandingToken.objects.filter(user_id=user_bd.id)
    for token in tokens:
      BlacklistedToken.objects.get_or_create(token=token)


user_service = UserService()
