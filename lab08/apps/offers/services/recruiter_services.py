from typing import Type
from ..models.Recruiter import Recruiter
from .base_services import BaseService

class RecruiterService(BaseService[Recruiter]):
    """
    Servicio encargado del mantenimiento de los perfiles de reclutadores.
    Hereda: obtener_todos(), obtener_por_id(), crear(), actualizar(), eliminar().
    """
    model: Type[Recruiter] = Recruiter