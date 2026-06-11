from typing import Type
from ..models.Company import Company
from .base_services import BaseService

class CompanyService(BaseService[Company]):
    """
    Servicio encargado de la gestión de información e infraestructura de empresas.
    """
    model: Type[Company] = Company
    
    # Hereda automáticamente: obtener_todos(), obtener_por_id(), crear(), actualizar(), eliminar()
    # Nota: El formateo a mayúsculas ya se ejecuta nativamente en el método save() del modelo Company.