from apps.jobs.schemas.location import LocationResponseDetail
from apps.jobs.services.location_service import location_service
from ninja import Router

router_locations = Router(tags=['Locations'])


@router_locations.get('', response=list[LocationResponseDetail])
def get_all(request):
  return location_service.get_all()
