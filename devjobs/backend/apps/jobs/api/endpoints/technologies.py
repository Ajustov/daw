from apps.jobs.schemas.technology import TechnologyResponse
from apps.jobs.services.technology_service import technology_service
from ninja import Router

router_technologies = Router(tags=['Technologies'])


@router_technologies.get('', response=list[TechnologyResponse])
def get_all(request):
  return technology_service.get_all()
