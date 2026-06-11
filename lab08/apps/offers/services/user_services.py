from typing import Any, Type
from django.core.exceptions import ValidationError
from ..models.User import User
from .base_services import BaseService

class UserService(BaseService[User]):
    """
    Servicio encargado del ciclo de vida y estado de activación de las cuentas de usuario.
    """
    model: Type[User] = User

    def cambiar_estado_activacion(self, pk: Any, activo: bool) -> User:
        """
        Suspende o activa lógicamente una cuenta de usuario sin borrar sus registros históricos.
        """
        usuario = self.obtener_por_id(pk)
        usuario.is_active = activo
        # Guardamos forzando la actualización de campos específicos de auditoría
        usuario.save(update_fields=['is_active', 'modified'])
        return usuario