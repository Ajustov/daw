from apps.jobs.schemas.user import UserResponsePrivate, UserUpdate
from apps.jobs.services.user_service import user_service
from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

router_users = Router(tags=['Users'])


@router_users.get('/me', auth=JWTAuth(), response=UserResponsePrivate)
def get_me(request):
  return request.auth


@router_users.patch('/me', auth=JWTAuth(), response=UserResponsePrivate)
def patch(request, user: UserUpdate):
  try:
    return user_service.patch(request.auth, user)
  except IntegrityError as e:
    raise HttpError(409, str(e))


@router_users.delete('/me', auth=JWTAuth(), response=UserResponsePrivate)
def deactivate(request):
  return user_service.deactivate(request.auth)
