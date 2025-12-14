"""
Routes Package - Classroom Explorer

[REFACTOR] Cambiado de Flask Blueprints a Python POO puro.
Exporta los handlers HTTP para la API.
"""

from .auth import AuthHandler, SessionStore, session_store
from .courses import CoursesHandler
from .materials import MaterialsHandler

__all__ = [
    "AuthHandler",
    "SessionStore",
    "session_store",
    "CoursesHandler",
    "MaterialsHandler",
]


