from typing import Any
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .base_views import BaseCRUDViewSet
from ..services.application_services import ApplicationService

class ApplicationViewSet(BaseCRUDViewSet):
    """
    Controlador REST para postulaciones. Hereda operaciones CRUD estándar 
    y añade flujos específicos de negocio.
    """
    serializer_class = None

    def get_servicio(self) -> ApplicationService:
        return ApplicationService()

    @action(detail=False, methods=['post'], url_path='postular')
    def postular(self, request: Any) -> Response:
        """
        Registra la intención de un candidato de aplicar a una vacante.
        Evita duplicidades controladas desde el servicio.
        """
        candidate_id = request.data.get('candidate_id')
        offer_id = request.data.get('offer_id')

        if not candidate_id or not offer_id:
            return Response({"error": "Los campos 'candidate_id' y 'offer_id' son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            app = self.get_servicio().crear_postulacion(
                candidate_id=candidate_id, 
                offer_id=offer_id, 
                user_ejecutor=request.user
            )
            return Response({"id": str(app.id), "message": "Postulación registrada con éxito."}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='mis-postulaciones')
    def mis_postulaciones(self, request: Any) -> Response:
        """
        CORREGIDO: Se agregó el método que faltaba.
        Recupera el historial detallado de aplicaciones del candidato autenticado.
        """
        if not request.user.is_authenticated:
            return Response({"error": "No autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            # Obtiene el historial a través del servicio
            historial = self.get_servicio().obtener_postulaciones_por_candidato(user_id=request.user.id)
            datos = [{
                "id": str(app.id),
                "offer_title": app.offer.title,
                "company_name": app.offer.recruiter.company.name,
                "status": app.status,
                "applied_at": app.created.strftime("%Y-%m-%d %H:%M:%S")
            } for app in historial]
            return Response(datos, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='cambiar-estado')
    def cambiar_estado(self, request: Any, pk: Any = None) -> Response:
        """
        Permite al reclutador avanzar o cambiar el estado de la postulación (reviewed, rejected, hired).
        """
        nuevo_estado = request.data.get('status')
        if not nuevo_estado:
            return Response({"error": "El parámetro 'status' es mandatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            app = self.get_servicio().actualizar_estado_postulacion(
                application_id=pk, 
                nuevo_estado=nuevo_estado
            )
            return Response({"id": str(app.id), "status": app.status, "message": "Estado actualizado correctamente."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)