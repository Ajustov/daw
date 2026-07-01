from apps.jobs.schemas.company import CompanyResponseDetail
from apps.jobs.services.company_service import company_service
from ninja import Router
from ninja_jwt.authentication import JWTAuth

router_companies = Router(tags=['Companies'])


@router_companies.get('/', auth=JWTAuth(), response=list[CompanyResponseDetail])
def get_all(request):
  return company_service.get_all()
