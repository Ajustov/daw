from typing import Any
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.http import Http404
from ..services.base_services import BaseService

class BaseCRUDViewSet(viewsets.GenericViewSet):
    """
    Controlador genérico abstracto DRF que mapea las acciones REST
    directamente hacia la lógica pura de la Capa de Servicios.
    """
    serializer_class = None  # Espacio reservado exclusivamente para tu compañero

    def get_servicio(self) -> BaseService:
        """Debe retornar una instancia de BaseService en los controladores hijos."""
        raise NotImplementedError("Cada ViewSet debe implementar obligatoriamente el método 'get_servicio()'.")

    def list(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        servicio = self.get_servicio()
        instancias = servicio.obtener_todos()
        # Simulación de respuesta estructurada limpia mientras se acoplan los Serializers
        datos = [{"id": str(obj.id), "str_representacion": str(obj)} for obj in instancias]
        return Response(datos, status=status.HTTP_200_OK)

    def create(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        servicio = self.get_servicio()
        try:
            # Se inyecta el usuario que realiza la acción como creador si el servicio lo requiere
            data = request.data.copy()
            instancia = servicio.crear(**data)
            return Response({"id": str(instancia.id), "message": "Creado con éxito."}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"errors": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request: Any, pk: Any = None, *args: Any, **kwargs: Any) -> Response:
        servicio = self.get_servicio()
        try:
            instancia = servicio.obtener_por_id(pk)
            return Response({"id": str(instancia.id), "str_representacion": str(obj for obj in [instancia])[0]}, status=status.HTTP_200_OK)
        except (ValidationError, Http404, Exception) as e:
            return Response({"error": "El recurso solicitado no existe."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request: Any, pk: Any = None, *args: Any, **kwargs: Any) -> Response:
        servicio = self.get_servicio()
        try:
            instancia = servicio.actualizar(pk, **request.data)
            return Response({"id": str(instancia.id), "message": "Actualizado de manera exitosa."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"errors": e.message_dict if hasattr(e, 'message_dict') else str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Any, pk: Any = None, *args: Any, **kwargs: Any) -> Response:
        servicio = self.get_servicio()
        try:
            servicio.eliminar(pk)
            return Response({"message": "Eliminado correctamente del sistema."}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)