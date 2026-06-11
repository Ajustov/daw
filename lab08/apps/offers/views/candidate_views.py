from typing import Any
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from django.core.exceptions import ValidationError
from .base_views import BaseCRUDViewSet
from ..services.candidate_services import CandidateService

class CandidateViewSet(BaseCRUDViewSet):
    """
    Endpoints REST para la administración de perfiles de candidatos y descarga directa de currículums.
    """
    serializer_class = None

    def get_servicio(self) -> CandidateService:
        return CandidateService()

    @action(detail=True, methods=['get'], url_path='descargar-cv')
    def descargar_cv(self, request: Any, pk: Any = None) -> Any:
        """
        Retorna un FileResponse que fuerza al navegador a realizar la descarga directa del PDF físico del CV.
        """
        servicio = self.get_servicio()
        try:
            # Obtiene el manejador binario abierto (rb) desde la capa de servicios
            file_handle, nombre_archivo = servicio.obtener_archivo_cv(candidate_id=pk)
            
            response = FileResponse(file_handle, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return response
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error de E/S en servidor: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)