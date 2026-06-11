from typing import Any
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from ..services.candidate_technology_services import CandidateTechnologyService

class CandidateTechnologyViewSet(viewsets.ViewSet):
    """
    Controlador dedicado a la vinculación y asignación masiva de tecnologías 
    a los perfiles profesionales de los candidatos.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.cand_tech_service = CandidateTechnologyService()

    def create(self, request: Any) -> Response:
        """
        Recibe un JSON con el ID del candidato y el bloque completo de tecnologías.
        Ejemplo: { "candidate_id": "UUID", "technologies": ["UUID1", "UUID2"] }
        """
        candidate_id = request.data.get('candidate_id')
        tecnologias_ids = request.data.get('technologies', [])

        if not candidate_id:
            return Response({"error": "El parámetro 'candidate_id' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            total_vinculados = self.cand_tech_service.actualizar_habilidades_candidato(
                candidate_id=candidate_id,
                lista_tecnologias_ids=tecnologias_ids
            )
            return Response({
                "message": "Habilidades técnicas del candidato actualizadas con éxito.",
                "candidate_id": str(candidate_id),
                "technologies_linked_count": total_vinculados
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error de consistencia de datos: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)