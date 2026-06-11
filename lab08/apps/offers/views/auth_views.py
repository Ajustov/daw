from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from ..services.auth_services import AuthService

class LoginView(APIView):
    """
    Endpoint POST para procesar credenciales de usuario y establecer cookies de sesión nativas.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.auth_service = AuthService()

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        try:
            # 1. Autenticar credenciales en la capa lógica pura
            user = self.auth_service.autenticar_usuario(request.data)
            
            # 2. Iniciar sesión en el backend HTTP con la sesión nativa de Django
            login(request, user)
            
            # 3. Resolver el rol del usuario autenticado para guiar adecuadamente el Frontend
            rol, perfil_id = self.auth_service.resolver_rol_usuario(user.id)
            
            return Response({
                "message": "Autenticación satisfactoria.",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "full_name": user.get_full_name(),
                    "role": rol,
                    "profile_id": str(perfil_id) if perfil_id else None
                }
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Endpoint POST para invalidar y destruir las cookies de sesión vigentes de Django.
    """
    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        logout(request)  # Elimina de manera segura la sesión del request actual
        return Response({"message": "Sesión cerrada de forma correcta."}, status=status.HTTP_200_OK)