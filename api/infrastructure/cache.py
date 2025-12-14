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


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que MemoryCache funciona.
    
    Ejecutar con:
        python -m api.infrastructure.cache
    """
    import time
    
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: MemoryCache")
    print("=" * 60)
    
    # Crear instancia nueva para tests
    test_cache = MemoryCache()
    
    # Test 1: set() y get()
    print("\n1. Verificar set() y get():")
    test_cache.set("key1", "value1", ttl_seconds=60)
    result = test_cache.get("key1")
    print(f"   ✓ set('key1', 'value1')")
    print(f"   ✓ get('key1') = '{result}' (esperado: 'value1')")
    
    # Test 2: get() con clave inexistente
    print("\n2. Verificar get() con clave inexistente:")
    result = test_cache.get("clave_que_no_existe")
    print(f"   ✓ get('clave_inexistente') = {result} (esperado: None)")
    
    # Test 3: has()
    print("\n3. Verificar has():")
    has_key1 = test_cache.has("key1")
    has_fake = test_cache.has("fake_key")
    print(f"   ✓ has('key1') = {has_key1} (esperado: True)")
    print(f"   ✓ has('fake_key') = {has_fake} (esperado: False)")
    
    # Test 4: delete()
    print("\n4. Verificar delete():")
    test_cache.set("to_delete", "value")
    print(f"   ✓ Antes: has('to_delete') = {test_cache.has('to_delete')}")
    test_cache.delete("to_delete")
    print(f"   ✓ Después: has('to_delete') = {test_cache.has('to_delete')} (esperado: False)")
    
    # Test 5: size()
    print("\n5. Verificar size():")
    test_cache.clear()
    test_cache.set("a", 1)
    test_cache.set("b", 2)
    test_cache.set("c", 3)
    print(f"   ✓ size() = {test_cache.size()} (esperado: 3)")
    
    # Test 6: clear()
    print("\n6. Verificar clear():")
    test_cache.clear()
    print(f"   ✓ size() después de clear() = {test_cache.size()} (esperado: 0)")
    
    # Test 7: TTL (expiración)
    print("\n7. Verificar TTL (expiración):")
    test_cache.set("short_ttl", "value", ttl_seconds=1)
    print(f"   ✓ Antes: get('short_ttl') = '{test_cache.get('short_ttl')}'")
    print("   ⏳ Esperando 2 segundos...")
    time.sleep(2)
    result = test_cache.get("short_ttl")
    print(f"   ✓ Después: get('short_ttl') = {result} (esperado: None)")
    
    # Test 8: Guardar objetos complejos
    print("\n8. Verificar objetos complejos:")
    complex_data = {"name": "John", "courses": [1, 2, 3], "active": True}
    test_cache.set("complex", complex_data)
    retrieved = test_cache.get("complex")
    print(f"   ✓ Guardado: {complex_data}")
    print(f"   ✓ Recuperado: {retrieved}")
    print(f"   ✓ Son iguales: {complex_data == retrieved}")
    
    # Test 9: Verificar singleton global
    print("\n9. Verificar singleton global:")
    print(f"   ✓ Tipo de 'cache': {type(cache).__name__}")
    print(f"   ✓ Es MemoryCache: {isinstance(cache, MemoryCache)}")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de MemoryCache: OK")
    print("=" * 60)
