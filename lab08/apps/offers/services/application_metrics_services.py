from typing import Any, Dict
from django.db.models import Count
from ..models.Application import Application

class ApplicationMetricsService:
    def obtener_kpis_reclutador(self, recruiter_id: Any) -> Dict[str, Any]:
        """
        Agrega contadores de postulaciones por estado para el dashboard.
        Transforma el QuerySet estructurado de Django en un diccionario clave-valor directo.
        """
        resultados = (
            Application.objects.filter(recruiter_id=recruiter_id)
            .values('status')
            .annotate(total=Count('id'))
        )
        
        # Mapeo limpio para el dashboard: {'pending': 5, 'reviewed': 2, ...}
        return {item['status']: item['total'] for item in resultados}