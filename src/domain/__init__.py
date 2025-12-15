"""
Domain Layer Package - Classroom Explorer

Esta capa contiene la lógica de negocio pura:
- Entities: Course, Material, MaterialType, CourseState
- Factories: CourseFactory, MaterialFactory
- Interfaces: ClassroomRepository (Port)

Esta capa NO depende de nada externo.
"""

from .entities import Course, Material, MaterialType, CourseState
from .factories import CourseFactory, MaterialFactory
from .interfaces import ClassroomRepository

__all__ = [
    # Entities
    "Course",
    "Material",
    "MaterialType",
    "CourseState",
    # Factories
    "CourseFactory",
    "MaterialFactory",
    # Interfaces
    "ClassroomRepository",
]
