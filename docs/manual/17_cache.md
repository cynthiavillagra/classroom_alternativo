# 📄 MemoryCache — Manual Técnico

**Archivo:** `api/infrastructure/cache.py`  
**Propósito:** Caché en memoria con TTL para reducir llamadas a APIs  
**Trazabilidad:** RNF-PERF01 (Performance), Optimización de API calls

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `datetime`, `timedelta`: Para calcular expiración
   - `Tuple`: Guardamos `(valor, fecha_expiracion)`
   - POR QUÉ no redis: Simple, sin infra externa para MVP

2. **Paso 2 — Definir la clase MemoryCache:**
   - Diccionario interno `_cache`
   - POR QUÉ privado (`_`): Encapsulación, acceso solo por métodos

3. **Paso 2.1 — Método `get()`:**
   - Verifica si existe y no expiró
   - Elimina si expiró (lazy cleanup)
   - POR QUÉ lazy: No ocupamos CPU limpiando proactivamente

4. **Paso 2.2 — Método `set()`:**
   - Guarda valor con fecha de expiración
   - TTL por defecto: 300 segundos (5 min)
   - POR QUÉ 5 min: Balance entre frescura y performance

5. **Paso 2.3 — Métodos auxiliares:**
   - `delete()`, `clear()`, `has()`, `size()`
   - POR QUÉ completos: Interface similar a Redis

6. **Paso 3 — Singleton global:**
   - Instancia `cache = MemoryCache()`
   - POR QUÉ: Un solo caché compartido en la app

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ datetime: Para calcular expiración de valores
from datetime import datetime, timedelta
from typing import Optional, Any, Dict, Tuple


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la clase MemoryCache
# ═══════════════════════════════════════════════════════════════
class MemoryCache:
    def __init__(self):
        # Diccionario: key -> (value, expiry_datetime)
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        value, expiry = self._cache[key]
        # Verificar expiración
        if datetime.now() > expiry:
            del self._cache[key]  # Lazy cleanup
            return None
        return value
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expiry)


# Paso 3: Singleton global
cache = MemoryCache()
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.infrastructure.cache
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: MemoryCache
============================================================

1. Verificar set() y get():
   ✓ set('key1', 'value1')
   ✓ get('key1') = 'value1' (esperado: 'value1')
   ...

✅ Prueba de MemoryCache: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ caché en memoria

| Beneficio | Explicación |
|-----------|-------------|
| **Sin infraestructura** | No necesita Redis, Memcached, etc. |
| **Simple** | Fácil de implementar y debuggear |
| **Rápido** | Acceso O(1) a memoria local |
| **Suficiente para MVP** | Mejora notable sin complejidad |

### ❌ POR QUÉ NO Redis (por ahora)

| Razón | Detalle |
|-------|---------|
| **Overkill** | Más infraestructura que gestionar |
| **Vercel limitation** | Serverless reinicia funciones, caché se pierde |
| **Costo** | Redis managed añade costo al proyecto |
| **MVP scope** | Optimizar prematuramente es contraproducente |

---

## 🎓 Conceptos Educativos

### TTL (Time To Live)

Cada valor tiene una "fecha de muerte":

```python
# Valor válido por 5 minutos
cache.set("user_123", data, ttl_seconds=300)

# Después de 5 min, get() retorna None
```

### Lazy Cleanup

No limpiamos proactivamente. Solo al acceder:

```python
def get(self, key):
    value, expiry = self._cache[key]
    if datetime.now() > expiry:
        del self._cache[key]  # Limpieza al acceder
        return None
    return value
```

Esto es más eficiente que limpiar periódicamente.

### Singleton Pattern

```python
# Una sola instancia global
cache = MemoryCache()

# Usada en toda la app
from api.infrastructure.cache import cache
cache.set("key", "value")
```
