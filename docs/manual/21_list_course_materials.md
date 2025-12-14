# 📄 ListCourseMaterials (Use Case) — Manual Técnico

**Archivo:** `api/application/use_cases/list_course_materials.py`  
**Propósito:** Use Case para listar materiales de un curso con filtros  
**Trazabilidad:** RF-M03 (Listar materiales), RF-M04 (Tipos), Clean Architecture

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `Material`, `MaterialType`: Entidades del dominio
   - `ClassroomRepository`: Interface (Dependency Injection)
   - POR QUÉ interface: Desacoplamos del repositorio concreto

2. **Paso 2 — Definir DTOs:**
   - `ListCourseMaterialsRequest`: course_id, access_token, filtros
   - `ListCourseMaterialsResponse`: materials, conteos, estadísticas
   - POR QUÉ DTOs: Encapsulan datos entre capas

3. **Paso 3 — Definir clase Use Case:**
   - Constructor recibe `ClassroomRepository`
   - Método `execute()` procesa la solicitud
   - POR QUÉ DI: Testeable con mock repository

4. **Paso 3.1 — Método `execute()`:**
   - Obtiene materiales del repositorio
   - Calcula conteo por tipo (antes de filtrar)
   - Aplica filtros (tipo, búsqueda)
   - Aplica límite si existe
   - Retorna Response DTO

5. **Paso 3.2 — Método `_apply_filters()`:**
   - Filtra por tipo de material
   - Busca en título y descripción
   - POR QUÉ case-insensitive: Mejor UX

6. **Paso 3.3 — Método `_count_by_type()`:**
   - Cuenta materiales por tipo
   - Retorna dict para estadísticas
   - POR QUÉ: Dashboard de materiales necesita estos conteos

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
from api.domain.entities import Material, MaterialType
from api.domain.interfaces import ClassroomRepository


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir DTOs
# ═══════════════════════════════════════════════════════════════
@dataclass
class ListCourseMaterialsRequest:
    course_id: str
    access_token: str
    filter_type: Optional[MaterialType] = None
    search_query: Optional[str] = None
    limit: Optional[int] = None

@dataclass
class ListCourseMaterialsResponse:
    materials: List[Material]
    total_count: int
    filtered_count: int
    type_counts: dict


# ═══════════════════════════════════════════════════════════════
# Paso 3: Definir el Use Case
# ═══════════════════════════════════════════════════════════════
class ListCourseMaterials:
    def __init__(self, repository: ClassroomRepository):
        self.repository = repository
    
    def execute(self, request: ListCourseMaterialsRequest) -> ListCourseMaterialsResponse:
        # Paso 3.1.1: Obtener materiales
        all_materials = self.repository.get_course_materials(...)
        
        # Paso 3.1.2: Contar por tipo (antes de filtrar)
        type_counts = self._count_by_type(all_materials)
        
        # Paso 3.1.3: Aplicar filtros
        filtered = self._apply_filters(all_materials, ...)
        
        # Paso 3.1.4: Aplicar límite
        if request.limit:
            filtered = filtered[:request.limit]
        
        return ListCourseMaterialsResponse(...)
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.application.use_cases.list_course_materials
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: ListCourseMaterials
============================================================

1. Ejecutar sin filtros:
   ✓ Total: 4
   ✓ Filtrados: 4
   ✓ Conteo por tipo: {'pdf': 1, 'video': 1, 'assignment': 1, 'link': 1}
   ...

✅ Prueba de ListCourseMaterials: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ filtros flexibles

| Beneficio | Explicación |
|-----------|-------------|
| **UX mejorada** | Usuario encuentra materiales rápido |
| **Búsqueda eficiente** | Filtrar en backend, no en frontend |
| **Reutilizable** | Mismos filtros desde API o CLI |
| **Escalable** | Agregar filtros no cambia arquitectura |

### ❌ POR QUÉ NO filtrar solo en frontend

| Problema | Impacto |
|----------|---------|
| **Lento** | Transferir todos los materiales para filtrar |
| **Duplicación** | Lógica de filtros en cada cliente |
| **Inconsistencia** | Cada cliente puede filtrar diferente |

---

## 🎓 Conceptos Educativos

### DTO Pattern

Los DTOs encapsulan datos entre capas sin lógica:

```python
# Request DTO (entrada)
request = ListCourseMaterialsRequest(
    course_id="123",
    access_token="token",
    filter_type=MaterialType.PDF
)

# Response DTO (salida)
response = ListCourseMaterialsResponse(
    materials=[...],
    total_count=10,
    filtered_count=3,
    type_counts={'pdf': 3}
)
```

### Search con Filtros

```python
def _apply_filters(self, materials, filter_type, search_query):
    result = materials
    
    # Filtro por tipo
    if filter_type:
        result = [m for m in result if m.type == filter_type]
    
    # Búsqueda en texto (case-insensitive)
    if search_query:
        query = search_query.lower()
        result = [m for m in result if query in m.title.lower()]
    
    return result
```
