from typing import Dict, Any
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models.User import User
from ..models.Candidate import Candidate
from ..models.Recruiter import Recruiter
from ..models.Company import Company

class RegistrationService:
    """
    Servicio transaccional para la creación compleja de cuentas con perfiles y roles.
    """

    @transaction.atomic
    def registrar_nuevo_candidato(self, datos_usuario: Dict[str, Any], datos_perfil: Dict[str, Any], archivo_cv: Any) -> Candidate:
        """
        Crea de forma atómica el User base, procesa el binario del CV y guarda el Candidate.
        """
        password = datos_usuario.pop('password', None)
        if not password:
            raise ValidationError("El password es requerido para registrar un usuario.")
            
        # 1. Crear e iniciar el usuario base
        user = User(**datos_usuario)
        user.set_password(password)
        user.full_clean()
        user.save()

        # 2. Preparar relaciones del perfil del Candidato
        datos_perfil['user'] = user          # CORREGIDO: 'user' en lugar de 'user_id'
        datos_perfil['created_id'] = user    # Asigna el usuario creador
        datos_perfil['modified_id'] = user   # Opcional: inicializa el modificador con el mismo creador
        
        if archivo_cv:
            datos_perfil['cv'] = archivo_cv

        # 3. Guardar entidad de negocio aplicando validadores personalizados del modelo
        candidato = Candidate(**datos_perfil)
        try:
            candidato.full_clean()
        except ValidationError as e:
            raise ValidationError(e.message_dict)
        
        candidato.save()
        return candidato

    @transaction.atomic
    def registrar_nuevo_reclutador(self, datos_usuario: Dict[str, Any], datos_perfil: Dict[str, Any]) -> Recruiter:
        """
        Crea el usuario base, localiza la compañía mediante su ID y consolida el perfil corporativo.
        """
        company_id = datos_perfil.pop('company_id', None)
        if not company_id:
            raise ValidationError("Debe proporcionar un 'company_id' válido para asociar al reclutador.")

        try:
            empresa = Company.objects.get(id=company_id)
        except (Company.DoesNotExist, ValidationError):
            raise ValidationError(f"La empresa con ID {company_id} no existe en los registros corporativos.")

        password = datos_usuario.pop('password', None)
        if not password:
            raise ValidationError("El password es requerido para registrar un usuario.")
            
        # 1. Crear el usuario del reclutador
        user = User(**datos_usuario)
        user.set_password(password)
        user.full_clean()
        user.save()

        # 2. Consolidar el perfil del Reclutador asociado
        datos_perfil['user'] = user          # CORREGIDO: 'user' en lugar de 'user_id'
        datos_perfil['company'] = empresa    # CORREGIDO: usar la relación 'company' directa
        datos_perfil['created_id'] = user 
        datos_perfil['modified_id'] = user

        reclutador = Recruiter(**datos_perfil)
        try:
            reclutador.full_clean()
        except ValidationError as e:
            raise ValidationError(e.message_dict)
            
        reclutador.save()
        return reclutador