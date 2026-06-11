from typing import Any, List, Type
from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ..models.Application import Application, Status
from ..models.Offer import Offer
from ..models.Candidate import Candidate
from ..models.Recruiter import Recruiter
from .base_services import BaseService

class ApplicationService(BaseService[Application]):
    model: Type[Application] = Application

    @transaction.atomic
    def crear_postulacion(self, candidate_id: Any, offer_id: Any, user_auth: Any) -> Application:
        """Registra la postulación evitando duplicados en la misma vacante."""
        if Application.objects.filter(candidate_id=candidate_id, offer_id=offer_id).exists():
            raise ValidationError("Ya te has postulado a esta vacante.")
            
        candidato = get_object_or_404(Candidate, id=candidate_id)
        oferta = get_object_or_404(Offer, id=offer_id)
        
        # Corrección lógica: Buscamos al reclutador dueño de la vacante para indexarlo 
        # directamente en la postulación. Esto previene fallos en el módulo de métricas.
        reclutador = Recruiter.objects.filter(id=oferta.recruiter_id).first()
            
        return super().crear(
            candidate_id=candidato,
            offer_id=oferta,
            recruiter_id=reclutador,
            created_id=user_auth,
            status=Status.PENDING
        )

    def actualizar_estado_postulacion(self, pk: Any, nuevo_estado: str) -> Application:
        """Avanza el estado del postulante en el embudo de selección."""
        app = self.obtener_por_id(pk)
        if nuevo_estado not in Status.values:
            raise ValidationError("Estado no válido.")
        app.status = nuevo_estado
        app.save(update_fields=['status'])
        return app