# 📄 GoogleClassroomRepository — Manual Técnico

**Archivo:** `api/infrastructure/repositories/google_classroom_repository.py`  
**Propósito:** Implementación concreta de ClassroomRepository usando Google API  
**Trazabilidad:** Hexagonal Architecture, Repository Pattern

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `ClassroomRepository`: Interface que implementamos
   - `GoogleClassroomClient`: Cliente HTTP para Google
   - `ClassroomMapper`: Convierte API → dominio
   - `cache`: Para caching de resultados
   - POR QUÉ composición: Cada componente tiene una responsabilidad

2. **Paso 2 — Implementar la interface:**
   - Hereda de `ClassroomRepository`
   - Debe implementar TODOS los métodos abstractos
   - POR QUÉ: Cumple el contrato del dominio

3. **Paso 2.1 — Constructor con dependencias:**
   - Crea `GoogleClassroomClient()` y `ClassroomMapper()`
   - POR QUÉ en constructor: Dependency Injection posible

4. **Paso 2.2 — Método `get_user_courses()`:**
   - Verifica caché primero
   - Llama a Google API si no está en caché
   - Mapea respuesta a entidades
   - Guarda en caché
   - POR QUÉ caché: Reduce llamadas a API

5. **Paso 2.3 — Método `get_course_materials()`:**
   - Combina courseWork y courseWorkMaterials
   - Ordena por fecha (más reciente primero)
   - POR QUÉ combinar: Google separa tareas de materiales

6. **Paso 3 — Manejo de errores:**
   - Convierte `GoogleAPIError` → `RepositoryError`
   - 404 → `CourseNotFoundError`
   - POR QUÉ: Dominio no conoce errores de Google

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque verifica estructura e implementación de interface. NO hace llamadas reales a Google porque requiere credenciales.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
from api.domain.interfaces import ClassroomRepository, RepositoryError
from api.infrastructure.google_classroom_client import GoogleClassroomClient
from api.infrastructure.mappers import ClassroomMapper
from api.infrastructure.cache import cache


# ═══════════════════════════════════════════════════════════════
# Paso 2: Implementar la interface del repositorio
# ═══════════════════════════════════════════════════════════════
class GoogleClassroomRepository(ClassroomRepository):
    
    def __init__(self):
        # Paso 2.1: Inyectar dependencias
        self.client = GoogleClassroomClient()
        self.mapper = ClassroomMapper()
    
    def get_user_courses(self, user_id: str, access_token: str) -> List[Course]:
        # Paso 2.2.1: Verificar caché
        cache_key = f"courses_user_{user_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Paso 2.2.2: Llamar a Google API
        api_response = self.client.list_courses(access_token)
        
        # Paso 2.2.3: Mapear a entidades de dominio
        courses = [
            self.mapper.api_course_to_domain(data)
            for data in api_response.get('courses', [])
        ]
        
        # Paso 2.2.4: Guardar en caché
        cache.set(cache_key, courses, ttl_seconds=Config.CACHE_TTL_SECONDS)
        return courses
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.infrastructure.repositories.google_classroom_repository
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: GoogleClassroomRepository
============================================================

1. Verificar instanciación:
   ✓ Repositorio creado: GoogleClassroomRepository
   ✓ Es ClassroomRepository: True
   ...

⚠️  NOTA: No se hicieron llamadas reales a Google API
✅ Prueba de GoogleClassroomRepository: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ separar Repository de Client

| Beneficio | Explicación |
|-----------|-------------|
| **Single Responsibility** | Client = HTTP, Repository = lógica |
| **Caching centralizado** | Repository maneja caché, client no |
| **Composición** | Cada pieza es testeable por separado |
| **Interface compliance** | Repository cumple contrato del dominio |

### ❌ POR QUÉ NO mezclar HTTP con lógica de caché

| Problema | Impacto |
|----------|---------|
| **Difícil de testear** | Hay que mockear HTTP Y caché |
| **Violación SRP** | Un archivo hace demasiado |
| **Reutilización difícil** | No puedes usar caché sin HTTP |

---

## 🎓 Conceptos Educativos

### Composición sobre Herencia

```python
# ✅ Composición (lo que hacemos)
class GoogleClassroomRepository:
    def __init__(self):
        self.client = GoogleClassroomClient()  # Tiene un client
        self.mapper = ClassroomMapper()         # Tiene un mapper

# ❌ Herencia (evitar)
class GoogleClassroomRepository(GoogleClassroomClient):
    # Es un client... pero también quiere ser mapper?
```

### Cache-Aside Pattern

1. Verificar caché
2. Si no está → llamar API → guardar en caché
3. Retornar resultado

```python
cached = cache.get(key)
if cached:
    return cached  # HIT
result = api.fetch()  # MISS
cache.set(key, result)
return result
```
