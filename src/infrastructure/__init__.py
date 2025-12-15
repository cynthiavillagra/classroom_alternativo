"""
Infrastructure Layer Package - Classroom Explorer

Esta capa contiene las implementaciones concretas de:
- Clientes HTTP (Google Classroom API)
- Repositorios (implementaciones de interfaces)
- Mappers (conversión de datos externos)
- Configuración y Caché
"""

from .config import Config
from .cache import cache, MemoryCache
from .google_classroom_client import GoogleClassroomClient, GoogleAPIError

__all__ = [
    "Config",
    "cache",
    "MemoryCache",
    "GoogleClassroomClient",
    "GoogleAPIError",
]
