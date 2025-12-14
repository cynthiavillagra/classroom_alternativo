# 📄 Course (Entidad) — Manual Técnico

**Archivo:** `api/domain/entities/course.py`  
**Propósito:** Entidad de dominio inmutable que representa un curso de Google Classroom  
**Trazabilidad:** RF-M02 (Listar cursos), CU-002, HU-002

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `dataclass`: Reduce boilerplate, genera `__init__`, `__repr__`, `__eq__`
   - `datetime`: Manejo correcto de fechas con timezone
   - `Optional`: Campos que pueden ser None de forma explícita
   - `CourseState`: Enum con estados del curso

2. **Paso 2 — Definir la clase con dataclass:**
   - Usamos `@dataclass(frozen=True)` para inmutabilidad
   - POR QUÉ frozen: Thread-safe, cacheable, previene bugs de mutación

3. **Paso 2.1 — Campos requeridos (sin default):**
   - `id`, `name`, `state`, `owner_id`, `created_at`, `updated_at`
   - POR QUÉ primero: Python exige campos sin default antes de campos con default

4. **Paso 2.2 — Campos opcionales (con default None):**
   - `section`, `description`
   - POR QUÉ Optional: Explícitamente indica que puede ser None

5. **Paso 3 — Validaciones en __post_init__:**
   - Validar ID no vacío
   - Validar nombre con mínimo 3 caracteres
   - Validar owner_id no vacío
   - Validar que updated_at >= created_at
   - POR QUÉ __post_init__: Se ejecuta después de `__init__`, ideal para frozen dataclass

6. **Paso 4 — Métodos de negocio:**
   - `is_active()`: Delega a CourseState
   - `is_visible()`: Delega a CourseState
   - `to_dict()`: Serialización controlada para JSON

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema. No reemplaza a los tests unitarios formales.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ dataclass: Reduce boilerplate
# POR QUÉ datetime: Manejo correcto de fechas
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .course_state import CourseState


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la entidad Course
# ═══════════════════════════════════════════════════════════════
# POR QUÉ frozen=True: Inmutabilidad (thread-safe, cacheable)
@dataclass(frozen=True)
class Course:
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Campos requeridos (sin default)
    # ───────────────────────────────────────────────────────────
    id: str
    name: str
    state: CourseState
    owner_id: str
    created_at: datetime
    updated_at: datetime
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.2: Campos opcionales (con default None)
    # ───────────────────────────────────────────────────────────
    section: Optional[str] = None
    description: Optional[str] = None
    
    # ───────────────────────────────────────────────────────────
    # Paso 3: Validaciones en __post_init__
    # ───────────────────────────────────────────────────────────
    def __post_init__(self):
        if not self.id or not self.id.strip():
            raise ValueError("Course ID no puede estar vacío")
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.domain.entities.course
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: Course
============================================================

1. Crear curso válido:
   ✓ Curso creado: Course: Matemáticas 3°A - Turno Mañana (ACTIVE)
   ...

✅ Prueba de Course: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ usar dataclass inmutable

| Beneficio | Explicación |
|-----------|-------------|
| **Inmutabilidad** | `frozen=True` previene modificaciones accidentales |
| **Thread-safe** | Seguro para uso concurrente |
| **Cacheable** | Puede usarse como key en diccionarios |
| **Menos bugs** | Estado predecible, sin mutaciones sorpresa |
| **Menos código** | No necesitas escribir `__init__`, `__repr__`, `__eq__` |

### ❌ POR QUÉ NO usar diccionario o clase mutable

| Problema | Ejemplo |
|----------|---------|
| **Modificación accidental** | `course["name"] = "otro"` cambia el estado |
| **Sin validación** | `course["id"] = ""` es válido pero incorrecto |
| **Sin autocomplete** | `course["nmae"]` no da error hasta runtime |
| **Sin encapsulación** | Lógica repartida en todo el código |

---

## 🎓 Conceptos Educativos

### Inmutabilidad con frozen=True

```python
# ❌ SIN frozen=True (mutable)
course.name = "Historia"  # ¡Modificación accidental!

# ✅ CON frozen=True (inmutable)
course.name = "Historia"  # FrozenInstanceError!
```

### Validación Fail-Fast

El principio "fail-fast" significa detectar errores lo antes posible:
- ✅ En `__post_init__`: Error inmediato al crear
- ❌ En uso posterior: Error en producción, difícil de debuggear
