from apps.jobs.models.location import Location


class LocationService:
  def get_all(self) -> list[Location]:
    return list(Location.objects.filter(status=True))


location_service = LocationService()
