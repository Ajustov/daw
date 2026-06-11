from typing import List, Any
from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ..models.Candidate import Candidate
from ..models.Technology import Technology
from ..models.CandidateTechnology import CandidateTechnology

class CandidateTechnologyService:
    """
    Servicio especializado en transacciones complejas para las habilidades del candidato.
    """

    @transaction.atomic
    def actualizar_habilidades_candidato(self, candidate_id: Any, lista_tecnologias_ids: List[Any]) -> int:
        """
        Limpia de forma atómica todas las tecnologías previas asociadas al candidato
        y registra el nuevo conjunto de competencias técnicas seleccionadas.
        """
        # 1. Asegurar la existencia del candidato
        candidato = get_object_or_404(Candidate, id=candidate_id)

        if not isinstance(lista_tecnologias_ids, list):
            raise ValidationError("La estructura de tecnologías proporcionada debe ser obligatoriamente una lista.")

        # 2. Eliminar registros obsoletos del candidato en la tabla intermedia
        CandidateTechnology.objects.filter(candidate_id=candidato).delete()

        # 3. Vincular masivamente el nuevo listado de aptitudes
        vinculos_creados = 0
        for tech_id in lista_tecnologias_ids:
            tecnologia = get_object_or_404(Technology, id=tech_id)
            CandidateTechnology.objects.create(candidate_id=candidato, technology_id=tecnologia)
            vinculos_creados += 1

        return vinculos_creados