from typing import Any
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .base_views import BaseCRUDViewSet
from ..services.offer_services import OfferService
from ..services.offer_technology_services import OfferTechnologyService

class OfferViewSet(BaseCRUDViewSet):
    """
    Controlador RESTful para la gestión de Ofertas de Trabajo (Vacantes).
    """
    serializer_class = None

    def get_servicio(self) -> OfferService:
        return OfferService()

    def list(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Lista ofertas aplicando filtros dinámicos mediante query parameters."""
        filtros = {
            'modality': request.query_params.get('modality'),
            'title': request.query_params.get('title'),
            'location': request.query_params.get('location'),
        }
        try:
            ofertas = self.get_servicio().obtener_vacantes_activas(filtros)
            data = [{"id": str(o.id), "title": o.title, "modality": o.modality} for o in ofertas]
            return Response(data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='cerrar-oferta')
    def cerrar_oferta(self, request: Any, pk: Any = None) -> Response:
        """Cambia el estado de una oferta a inactiva de forma segura."""
        try:
            self.get_servicio().marcar_oferta_como_cerrada(pk)
            return Response({"message": "Oferta cerrada correctamente."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='vincular-tecnologias')
    def vincular_tecnologias(self, request: Any, pk: Any = None) -> Response:
        """Asocia masivamente un conjunto de tecnologías a la oferta especificada."""
        ids = request.data.get('technology_ids', [])
        try:
            count = OfferTechnologyService().vincular_tecnologias_a_oferta(pk, ids)
            return Response({"message": f"Se vincularon {count} tecnologías a la oferta."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)