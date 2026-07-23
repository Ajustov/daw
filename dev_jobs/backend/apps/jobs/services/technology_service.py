from apps.jobs.models.technology import Technology


class TechnologyService:
  def get_all(self) -> list[Technology]:
    return list(Technology.objects.filter(status=True))


technology_service = TechnologyService()
