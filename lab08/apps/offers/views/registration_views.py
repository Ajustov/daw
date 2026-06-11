from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.exceptions import ValidationError
from ..services.registration_services import RegistrationService

class RegistroCandidatoView(APIView):
    """
    Endpoint POST habilitado para recibir multipart de formularios (Campos de texto + binario PDF del CV).
    """
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.registration_service = RegistrationService()

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        # Extraemos los datos de usuario directamente de request.data (más seguro en DRF)
        datos_usuario = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
            "first_name": request.data.get("first_name", ""),
            "last_name": request.data.get("last_name", "")
        }
        
        # SOPORTE FLEXIBLE: Buscamos en snake_case o CamelCase para evitar errores desde Postman
        experience_years = request.data.get("experience_years")
        if experience_years is None:
            experience_years = request.data.get("experienceYears")
        
        # Dejamos este diccionario con la metadata del perfil mapeada al modelo
        datos_perfil = {
            "description": request.data.get("description", None),
            "seniority": request.data.get("seniority"),
            "experience_years": experience_years,  # Mapeado correctamente
        }

        archivo_cv = request.FILES.get("cv")

        try:
            nuevo_candidato = self.registration_service.registrar_nuevo_candidato(
                datos_usuario=datos_usuario,
                datos_perfil=datos_perfil,
                archivo_cv=archivo_cv
            )
            return Response({
                "message": "Cuenta de Candidato creada de forma exitosa.",
                "candidate_id": str(nuevo_candidato.id)
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegistroReclutadorView(APIView):
    """
    Endpoint POST exclusivo para dar de alta perfiles de Reclutadores asociados a una Compañía corporativa.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.registration_service = RegistrationService()

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        datos_usuario = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password"),
            "first_name": request.data.get("first_name", ""),
            "last_name": request.data.get("last_name", "")
        }
        
        datos_perfil = {
            "company_id": request.data.get("company_id"),
            "description": request.data.get("description", None)
        }

        try:
            nuevo_reclutador = self.registration_service.registrar_nuevo_reclutador(
                datos_usuario=datos_usuario,
                datos_perfil=datos_perfil
            )
            return Response({
                "message": "Cuenta de Reclutador creada de forma exitosa.",
                "recruiter_id": str(nuevo_reclutador.id)
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({"errors": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)