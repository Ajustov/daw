from apps.jobs.schemas.technology import TechnologyResponse
from apps.jobs.services.technology_service import technology_service
from ninja import Router
from ninja_jwt.authentication import JWTAuth

router_technologies = Router(tags=['Technologies'])


@router_technologies.get('/', auth=JWTAuth(), response=list[TechnologyResponse])
def get_all(request):
  return technology_service.get_all()
