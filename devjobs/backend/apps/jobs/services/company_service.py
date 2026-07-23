from apps.jobs.models.company import Company


class CompanyService:
  def get_all(self) -> list[Company]:
    return list(Company.objects.filter(status=True))


company_service = CompanyService()
