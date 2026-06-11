from typing import TypeVar, Generic, List, Type, Any, Optional
from django.db import models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

# Definimos el tipo genérico vinculado a los modelos de Django
M = TypeVar('M', bound=models.Model)

class BaseService(Generic[M]):
    """
    Clase Madre de Servicios con operaciones CRUD genéricas automatizadas.
    """
    model: Type[M]

    def __init__(self) -> None:
        if not hasattr(self, 'model') or self.model is None:
            raise NotImplementedError("Cada servicio derivado debe definir el atributo de clase 'model'.")

    def obtener_todos(self) -> List[M]:
        """Recupera todos los registros del modelo."""
        return list(self.model.objects.all())

    def obtener_por_id(self, pk: Any) -> M:
        """Recupera un registro por su clave primaria o lanza 404."""
        return get_object_or_404(self.model, pk=pk)

    def crear(self, **datos: Any) -> M:
        """Crea una nueva instancia del modelo y ejecuta sus validaciones."""
        instancia = self.model(**datos)
        instancia.full_clean()
        instancia.save()
        return instancia

    def actualizar(self, pk: Any, **datos: Any) -> M:
        """Actualiza un registro existente de forma parcial y segura."""
        instancia = self.obtener_por_id(pk)
        for campo, valor in datos.items():
            if hasattr(instancia, campo):
                setattr(instancia, campo, valor)
        instancia.full_clean()
        instancia.save()
        return instancia

    def eliminar(self, pk: Any) -> None:
        """Elimina un registro físico por su clave primaria."""
        instancia = self.obtener_por_id(pk)
        instancia.delete()