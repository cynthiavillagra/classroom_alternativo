"""
Domain Entities Package - Classroom Explorer

Este paquete contiene las entidades de dominio del sistema.

POR QUÉ SÍ este archivo __init__.py:
✅ Convierte la carpeta en un módulo Python
✅ Permite imports limpios: from src.domain.entities import Course
✅ Centraliza las exportaciones del módulo
✅ Documenta qué entidades están disponibles

POR QUÉ NO dejarlo vacío:
❌ Imports más verbosos: from src.domain.entities.course import Course
❌ No hay documentación del módulo
❌ No hay control sobre qué se exporta
"""

from .course import Course
from .material import Material
from .material_type import MaterialType
from .course_state import CourseState

__all__ = [
    "Course",
    "Material",
    "MaterialType",
    "CourseState",
]
