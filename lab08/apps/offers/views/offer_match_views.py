from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from ..services.offer_match_services import OfferMatchService

class OfertasSugeridasView(APIView):
    """
    Endpoint dinámico para calcular y retornar de forma ágil las vacantes ideales 
    para un candidato en base a su afinidad técnica.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.match_service = OfferMatchService()

    def get(self, request: Any, candidate_id: Any) -> Response:
        try:
            ofertas = self.match_service.calcular_ofertas_sugeridas(candidate_id)
            
            data = [
                {
                    "id": str(o.id),
                    "title": o.title,
                    "relevance_score": getattr(o, 'coincidencias', 0)
                } for o in ofertas
            ]
            return Response(data, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)