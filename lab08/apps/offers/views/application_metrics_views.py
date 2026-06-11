from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from ..services.application_metrics_services import ApplicationMetricsService

class DashboardMetricasView(APIView):
    """
    Endpoint analítico que expone los KPIs de postulaciones para el reclutador corporativo.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.metrics_service = ApplicationMetricsService()

    def get(self, request: Any, recruiter_id: Any) -> Response:
        try:
            # Invoca la lógica analítica de negocio agregada en BD
            metrics = self.metrics_service.obtener_kpis_reclutador(recruiter_id=recruiter_id)
            return Response(metrics, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error al procesar métricas: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)