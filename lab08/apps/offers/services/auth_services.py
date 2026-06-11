from typing import Optional, Dict, Any, Tuple
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from ..models.Candidate import Candidate
from ..models.Recruiter import Recruiter

class AuthService:
    """
    Servicio encargado de la lógica pura de autenticación y mapeo de roles de usuario.
    """

    def autenticar_usuario(self, datos_credenciales: Dict[str, Any]) -> AbstractUser:
        """
        Valida las credenciales en el motor de Django.
        Eleva un ValidationError de negocio si falla.
        """
        username = datos_credenciales.get('username')
        password = datos_credenciales.get('password')

        if not username or not password:
            raise ValidationError("Se requieren obligatoriamente 'username' y 'password'.")

        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError("Las credenciales proporcionadas son inválidas.")
        
        if not user.is_active:
            raise ValidationError("Esta cuenta de usuario se encuentra suspendida.")

        return user

    def resolver_rol_usuario(self, user_id: Any) -> Tuple[str, Optional[Any]]:
        """
        Verifica iterativamente si el ID pertenece a un Candidato o Reclutador.
        Retorna una tupla: (nombre_del_rol, id_del_perfil_especifico).
        """
        # 1. Comprobamos si es Candidato
        candidato = Candidate.objects.filter(user_id=user_id).first()
        if candidato:
            return "candidate", candidato.id

        # 2. Comprobamos si es Reclutador
        reclutador = Recruiter.objects.filter(user_id=user_id).first()
        if reclutador:  # Corrección de NameError (estaba como 'recruiter')
            return "recruiter", reclutador.id

        # 3. Si es Superusuario o Staff sin perfil asociado
        return "admin", None