from typing import Type, List, Dict, Any
from ..models.Offer import Offer
from .base_services import BaseService

class OfferService(BaseService[Offer]):
    model: Type[Offer] = Offer

    def obtener_vacantes_activas(self, filtros: Dict[str, Any]) -> List[Offer]:
        """
        Filtra ofertas activas basándose en parámetros opcionales enviados desde el frontend.
        """
        queryset = self.model.objects.filter(status=True)
        
        if filtros.get('modality'):
            queryset = queryset.filter(modality=filtros['modality'])
        if filtros.get('title'):
            queryset = queryset.filter(title__icontains=filtros['title'])
        if filtros.get('location'):
            queryset = queryset.filter(location__icontains=filtros['location'])
            
        return list(queryset.select_related('created_id'))

    def marcar_oferta_como_cerrada(self, pk: Any) -> Offer:
        """
        Cambia el estado de una oferta a inactiva y actualiza el registro.
        """
        oferta = self.obtener_por_id(pk)
        oferta.status = False
        # Guardamos sin update_fields para garantizar que campos auto_now como 'modified' se actualicen
        oferta.save()
        return oferta