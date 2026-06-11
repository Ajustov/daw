from typing import Any
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .base_views import BaseCRUDViewSet
from ..services.technology_services import TechnologyService

class TechnologyViewSet(BaseCRUDViewSet):
    """
    Endpoints REST para el control y filtrado dinámico del diccionario global de tecnologías.
    """
    serializer_class = None

    def get_servicio(self) -> TechnologyService:
        return TechnologyService()

    def list(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Sobrescribe la acción de listado genérico para permitir búsquedas dinámicas seguras mediante query params (?search=python).
        """
        termino_busqueda = request.query_params.get('search', '')
        try:
            servicio = self.get_servicio()
            resultados = servicio.buscar_por_nombre(termino_busqueda)
            datos = [{"id": str(obj.id), "name": obj.name} for obj in resultados]
            return Response(datos, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)