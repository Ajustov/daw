from typing import List, Any
from django.db.models import Count
from ..models.Offer import Offer
from ..models.CandidateTechnology import CandidateTechnology

class OfferMatchService:
    def calcular_ofertas_sugeridas(self, candidate_id: Any) -> List[Offer]:
        """
        Recomienda ofertas basándose en las tecnologías compartidas.
        Ordena por mayor coincidencia de habilidades de forma eficiente.
        """
        # 1. Obtener de manera plana los IDs de las tecnologías que posee el candidato
        tech_ids = CandidateTechnology.objects.filter(
            candidate_id=candidate_id
        ).values_list('technology_id', flat=True)

        # 2. Si el candidato no tiene tecnologías registradas, retornamos una lista vacía
        if not tech_ids:
            return []

        # 3. Buscar ofertas activas que soliciten al menos una de esas tecnologías,
        # anotando el conteo de coincidencias y ordenando descendentemente.
        return list(
            Offer.objects.filter(status=True, offertechnology__technology_id__in=tech_ids)
            .annotate(coincidencias=Count('offertechnology'))
            .order_by('-coincidencias')
            .distinct()
        )