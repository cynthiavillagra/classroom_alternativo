# 📄 ListUserCourses (Use Case) — Manual Técnico

**Archivo:** `api/application/use_cases/list_user_courses.py`  
**Propósito:** Use Case para listar cursos de un usuario con filtros  
**Trazabilidad:** RF-M02 (Listar cursos), CU-002, Clean Architecture

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `dataclass`: Para Request/Response DTOs simples
   - `ClassroomRepository`: Interface (Dependency Injection)
   - POR QUÉ interface: Desacoplamos del repositorio concreto

2. **Paso 2 — Definir DTOs:**
   - `ListUserCoursesRequest`: Entrada del use case
   - `ListUserCoursesResponse`: Salida del use case
   - POR QUÉ DTOs: Encapsulan datos entre capas

3. **Paso 3 — Definir clase Use Case:**
   - Constructor recibe `ClassroomRepository`
   - Método `execute()` procesa la solicitud
   - POR QUÉ DI: Testeable con mock repository

4. **Paso 3.1 — Método `execute()`:**
   - Obtiene cursos del repositorio
   - Aplica filtros (archived, state)
   - Calcula estadísticas
   - Retorna Response DTO

5. **Paso 3.2 — Método `_apply_filters()`:**
   - Filtra por estado específico
   - Excluye archivados si se solicita
   - Solo muestra cursos visibles
   - POR QUÉ privado: Lógica interna

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Usa un MockRepository para probar el Use Case sin depender de infraestructura real.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
from dataclasses import dataclass
from api.domain.interfaces import ClassroomRepository


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir DTOs
# ═══════════════════════════════════════════════════════════════
@dataclass
class ListUserCoursesRequest:
    user_id: str
    access_token: str
    include_archived: bool = True
    filter_state: Optional[CourseState] = None

@dataclass
class ListUserCoursesResponse:
    courses: List[Course]
    total_count: int
    active_count: int
    archived_count: int


# ═══════════════════════════════════════════════════════════════
# Paso 3: Definir el Use Case
# ═══════════════════════════════════════════════════════════════
class ListUserCourses:
    def __init__(self, repository: ClassroomRepository):
        # Dependency Injection
        self.repository = repository
    
    def execute(self, request: ListUserCoursesRequest) -> ListUserCoursesResponse:
        # Paso 3.1.1: Obtener cursos del repositorio
        all_courses = self.repository.get_user_courses(
            user_id=request.user_id,
            access_token=request.access_token
        )
        
        # Paso 3.1.2: Aplicar filtros
        filtered = self._apply_filters(all_courses, ...)
        
        # Paso 3.1.3: Calcular estadísticas y retornar
        return ListUserCoursesResponse(...)
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.application.use_cases.list_user_courses
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: ListUserCourses
============================================================

1. Ejecutar con include_archived=True:
   ✓ Total: 3
   ✓ Activos: 2
   ✓ Archivados: 1
   ...

✅ Prueba de ListUserCourses: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ separar en Use Case

| Beneficio | Explicación |
|-----------|-------------|
| **Single Responsibility** | Use case solo orquesta |
| **Testeable** | Mock del repositorio en tests |
| **Reutilizable** | Desde API REST, CLI, cron, etc. |
| **Clean Architecture** | Application Layer bien definida |

### ❌ POR QUÉ NO poner lógica en el Route

| Problema | Impacto |
|----------|---------|
| **Fat controllers** | Routes con 200+ líneas |
| **Difícil de testear** | Hay que levantar Flask |
| **No reutilizable** | Solo funciona vía HTTP |
| **Violación SRP** | Route hace HTTP + lógica |

---

## 🎓 Conceptos Educativos

### Use Case Pattern

Un Use Case representa UNA operación de negocio:

```
Request → Use Case → Response
            ↓
        Repository
```

### Dependency Injection

El Use Case NO crea el repositorio, lo RECIBE:

```python
# ✅ Inyección (correcto)
class ListUserCourses:
    def __init__(self, repository: ClassroomRepository):
        self.repository = repository

# ❌ Creación directa (acoplado)
class ListUserCourses:
    def __init__(self):
        self.repository = GoogleClassroomRepository()  # Acoplado!
```

Con DI podemos inyectar un mock en tests.
