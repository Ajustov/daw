from typing import Any
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .base_views import BaseCRUDViewSet
from ..services.user_services import UserService

class UserViewSet(BaseCRUDViewSet):
    """
    Endpoints REST para la administración y control de usuarios del sistema.
    """
    serializer_class = None

    def get_servicio(self) -> UserService:
        return UserService()

    @action(detail=True, methods=['post'], url_path='cambiar-estado')
    def cambiar_estado(self, request: Any, pk: Any = None) -> Response:
        """
        Endpoint seguro para activar o suspender una cuenta de usuario mitigando caídas descontroladas.
        """
        activo = request.data.get('is_active', True)
        try:
            servicio = self.get_servicio()
            usuario = servicio.cambiar_estado_activacion(pk, activo)
            return Response({
                "message": f"El estado del usuario ha sido modificado a: {usuario.is_active}"
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)