from apps.jobs.schemas.user import UserCreate, UserResponsePrivate
from apps.jobs.services.user_service import user_service
from django.db import IntegrityError
from ninja import Router
from ninja.errors import HttpError

router_auth = Router(tags=['Auth'])


@router_auth.post('/register', response={201: UserResponsePrivate})
def register(request, user: UserCreate):
  try:
    return user_service.create(user)
  except IntegrityError:
    raise HttpError(409, 'El usuario ya existe')


# Los demás endpoinsts no los da ninja-extras

# login -> pair
# refresh
# ? verify, es cuando no quieres llamar a ningun endpoint pero quieres confirmar que el access token es valido
# logout, no existe porque el access/refresh token son JWT
