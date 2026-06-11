from .base_views import BaseCRUDViewSet
from ..services.recruiter_services import RecruiterService

class RecruiterViewSet(BaseCRUDViewSet):
    """
    Endpoints RESTful automáticos para el mantenimiento y consulta de perfiles de Reclutadores.
    CORREGIDO: Se eliminó importación huérfana de modelo para garantizar consistencia.
    """
    serializer_class = None

    def get_servicio(self) -> RecruiterService:
        return RecruiterService()