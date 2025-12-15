"""
Domain Interfaces Package - Classroom Explorer

Este paquete contiene las interfaces (Ports) del dominio.

POR QUÉ SÍ usar interfaces (Ports):
✅ Define contratos que la infraestructura debe cumplir
✅ Permite cambiar implementaciones sin afectar el dominio
✅ Facilita testing con mocks
✅ Invierte las dependencias (Dependency Inversion Principle)
"""

from .classroom_repository import (
    ClassroomRepository,
    RepositoryError,
    CourseNotFoundError,
    MaterialNotFoundError,
    UnauthorizedError
)

__all__ = [
    "ClassroomRepository",
    "RepositoryError",
    "CourseNotFoundError",
    "MaterialNotFoundError",
    "UnauthorizedError",
]
