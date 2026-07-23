from apps.jobs.api.permissions import UserAuth
from apps.jobs.schemas.user import (
  UserResponseMe,
  UserResponsePrivate,
  UserUpdate,
  UserUpdatePassword,
)
from apps.jobs.services.user_service import user_service
from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError

router_users = Router(tags=['Users'])


@router_users.get('/me', auth=UserAuth(), response=UserResponseMe)
def get_me(request):
  return user_service.get_me(request.auth)


@router_users.patch('/me/password', auth=UserAuth(), response={204: None})
def patch_password(request, data: UserUpdatePassword):
  try:
    user_service.patch_password(request.auth, data)
  except ValueError as e:
    raise HttpError(400, str(e))


@router_users.patch('/me', auth=UserAuth(), response=UserResponsePrivate)
def patch(request, user: UserUpdate):
  try:
    return user_service.patch(request.auth, user)
  except IntegrityError as e:
    raise HttpError(409, str(e))


@router_users.delete('/me', auth=UserAuth(), response={204: None})
def deactivate(request):
  user_service.deactivate(request.auth)
