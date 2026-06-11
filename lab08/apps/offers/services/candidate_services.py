from typing import Any, Type, Tuple
from django.core.exceptions import ValidationError
from django.core.files.base import File
from ..models.Candidate import Candidate
from .base_services import BaseService

class CandidateService(BaseService[Candidate]):
    """
    Servicio operativo para perfiles de candidatos y extracción segura de adjuntos.
    """
    model: Type[Candidate] = Candidate

    def obtener_archivo_cv(self, candidate_id: Any) -> Tuple[File, str]:
        """
        Localiza al candidato y extrae el puntero de lectura en modo binario (rb) de su CV.
        Retorna una tupla con el File object y el nombre del archivo.
        """
        candidato = self.obtener_por_id(candidate_id)
        
        if not candidato.cv:
            raise ValidationError("El candidato solicitado no cuenta con un archivo de CV cargado en el sistema.")
            
        try:
            file_handle = candidato.cv.open('rb')  # Abre de forma segura el flujo binario desde el storage
            nombre_archivo = f"CV_{candidato.id}.pdf"
            return file_handle, nombre_archivo
        except Exception as e:
            raise ValidationError(f"No se pudo acceder físicamente al archivo almacenado: {str(e)}")