from apps.offers.views.base_views import BaseCRUDViewSet         
from ..services.company_services import CompanyService

class CompanyViewSet(BaseCRUDViewSet):
    """
    Endpoints RESTful automáticos (/api/companies/) para la administración y
    registro de entidades corporativas. Delega el guardado en mayúsculas al servicio.
    """
    serializer_class = None

    def get_servicio(self) -> CompanyService:
        return CompanyService()