"""
Memory Cache - Classroom Explorer

Caché simple en memoria con TTL (Time To Live).

POR QUÉ SÍ caché en memoria:
✅ Reduce llamadas a Google API
✅ Mejora performance
✅ No requiere infraestructura externa (Redis, Memcached)
✅ Simple de implementar y mantener

POR QUÉ NO Redis/Memcached (por ahora):
❌ Overkill para MVP
❌ Más infraestructura que gestionar
❌ Vercel Serverless reinicia funciones (caché se pierde igual)

LIMITACIÓN:
• En Vercel, cada función tiene su propia memoria
• El caché no se comparte entre requests diferentes
• Aceptable para MVP (cada usuario tiene su caché)
"""

from datetime import datetime, timedelta
from typing import Optional, Any, Dict, Tuple


class MemoryCache:
    """
    Caché simple en memoria con TTL.
    
    Implementa un diccionario con expiración automática de valores.
    """
    
    def __init__(self):
        """Inicializa el caché vacío."""
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor del caché si no expiró.
        
        Args:
            key: Clave del caché
        
        Returns:
            Valor si existe y no expiró, None en caso contrario
        
        Example:
            >>> cache = MemoryCache()
            >>> cache.set("user_123", {"name": "John"}, ttl_seconds=60)
            >>> cache.get("user_123")  # {"name": "John"}
            >>> # Después de 60 segundos:
            >>> cache.get("user_123")  # None
        """
        if key not in self._cache:
            return None
        
        value, expiry = self._cache[key]
        
        # Verificar si expiró
        if datetime.now() > expiry:
            # Expiró, eliminar
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """
        Guarda un valor en caché con TTL.
        
        Args:
            key: Clave del caché
            value: Valor a guardar (puede ser cualquier tipo)
            ttl_seconds: Tiempo de vida en segundos (default: 5 min)
        
        Example:
            >>> cache = MemoryCache()
            >>> cache.set("courses", [course1, course2], ttl_seconds=300)
        """
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """
        Elimina una clave del caché.
        
        Args:
            key: Clave a eliminar
        
        Example:
            >>> cache.delete("user_123")
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """
        Limpia todo el caché.
        
        Example:
            >>> cache.clear()  # Elimina todas las entradas
        """
        self._cache.clear()
    
    def has(self, key: str) -> bool:
        """
        Verifica si una clave existe y no expiró.
        
        Args:
            key: Clave a verificar
        
        Returns:
            bool: True si existe y no expiró
        
        Example:
            >>> cache.has("user_123")  # True o False
        """
        return self.get(key) is not None
    
    def size(self) -> int:
        """
        Retorna el número de entradas en caché (incluyendo expiradas).
        
        Returns:
            int: Número de entradas
        """
        return len(self._cache)


# Instancia global (singleton)
cache = MemoryCache()
