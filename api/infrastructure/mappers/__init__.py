"""
Infrastructure Mappers Package - Classroom Explorer

Este paquete contiene los mappers (Adapter Pattern) para convertir
datos externos a entidades de dominio.
"""

from .classroom_mapper import ClassroomMapper

__all__ = [
    "ClassroomMapper",
]
