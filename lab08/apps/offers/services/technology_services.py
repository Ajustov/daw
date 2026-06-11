from typing import List, Type
from ..models.Technology import Technology
from .base_services import BaseService

class TechnologyService(BaseService[Technology]):
    """
    Servicio encargado del catálogo global de tecnologías disponibles.
    """
    model: Type[Technology] = Technology

    def buscar_por_nombre(self, termino: str) -> List[Technology]:
        """
        Realiza búsquedas parciales e insensibles a mayúsculas para autocompletado en el frontend.
        """
        if not termino or not termino.strip():
            return list(self.model.objects.filter(status=True))
        
        # Limpiamos los espacios en blanco del término de búsqueda
        return list(self.model.objects.filter(name__icontains=termino.strip(), status=True))