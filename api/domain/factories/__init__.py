"""
Domain Factories Package - Classroom Explorer

Este paquete contiene las factories para crear entidades de dominio.

POR QUÉ SÍ usar Factory Pattern:
✅ Centraliza la creación de entidades complejas
✅ Encapsula validaciones y transformaciones
✅ Facilita crear entidades desde diferentes fuentes (API, tests, etc.)
✅ Permite cambiar la lógica de creación sin afectar el resto del código
"""

from .course_factory import CourseFactory
from .material_factory import MaterialFactory

__all__ = [
    "CourseFactory",
    "MaterialFactory",
]
