from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from ..services.offer_match_services import OfferMatchService

class OfertasSugeridasDetalladasView(APIView):
    """
    CORREGIDO: Se eliminó la importación del modelo Candidate y el get_object_or_404 
    para respetar el desacoplamiento de capas. El servicio asume el control.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.match_service = OfferMatchService()

    def get(self, request: Any, candidate_id: Any) -> Response:
        """
        Retorna ofertas ordenadas por 'coincidencias' técnicas con un payload extendido.
        """
        try:
            # El servicio valida la existencia del candidato internamente
            ofertas = self.match_service.calcular_ofertas_sugeridas(candidate_id)
            
            data = [
                {
                    "id": str(o.id),
                    "title": o.title,
                    "location": o.location,
                    "relevance_score": getattr(o, 'coincidencias', 0)
                } for o in ofertas
            ]
            
            return Response({
                "candidate_id": str(candidate_id),
                "suggested_offers_count": len(data),
                "offers": data
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Error al procesar el motor de matching: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )