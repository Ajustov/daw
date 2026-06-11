from typing import List, Any
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from ..models.Offer import Offer
from ..models.Technology import Technology
from ..models.OfferTechnology import OfferTechnology

class OfferTechnologyService:
    @transaction.atomic
    def vincular_tecnologias_a_oferta(self, offer_id: Any, lista_tecnologias_ids: List[Any]) -> int:
        """
        Sincroniza los requisitos técnicos de una oferta en lote sin consultas N+1 a la DB.
        """
        oferta = get_object_or_404(Offer, id=offer_id)
        
        # 1. Limpieza atómica de requisitos técnicos previos
        OfferTechnology.objects.filter(offer_id=oferta).delete()
        
        if not lista_tecnologias_ids:
            return 0

        # 2. Optimización: Traer todas las tecnologías válidas en una sola consulta
        tecnologias_existentes = Technology.objects.filter(id__in=lista_tecnologias_ids)
        
        # Validación opcional: Verificar consistencia en la cantidad solicitada vs existente
        if len(tecnologias_existentes) != len(set(lista_tecnologias_ids)):
            raise ValidationError("Una o más tecnologías proporcionadas no existen en el sistema.")
        
        # 3. Creación en bloque mediante bulk_create de manera eficiente
        vinculos = [
            OfferTechnology(offer_id=oferta, technology_id=tech)
            for tech in tecnologias_existentes
        ]
        OfferTechnology.objects.bulk_create(vinculos)
        return len(vinculos)