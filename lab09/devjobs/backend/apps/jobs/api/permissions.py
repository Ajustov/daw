from apps.jobs.models.candidate import Candidate
from apps.jobs.models.recruiter import Recruiter
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth


class RecruiterAuth(JWTAuth):
  def authenticate(self, request, token) -> Recruiter:
    # Usamos el authenticate del JWTAuth, que valida y devuelve el user
    user = super().authenticate(request, token)
    recruiter = Recruiter.objects.filter(user=user, status=True).first()
    if not recruiter:
      raise HttpError(403, 'No tienes perfil de recruiter')
    return recruiter


class CandidateAuth(JWTAuth):
  def authenticate(self, request, token) -> Candidate:
    # Usamos el authenticate del JWTAuth, que valida y devuelve el user
    user = super().authenticate(request, token)
    candidate = Candidate.objects.filter(user=user, status=True).first()
    if not candidate:
      raise HttpError(403, 'No tienes perfil de candidate')
    return candidate
