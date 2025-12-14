# 📄 Material (Entidad) — Manual Técnico

**Archivo:** `api/domain/entities/material.py`  
**Propósito:** Entidad de dominio inmutable que representa un material de curso  
**Trazabilidad:** RF-M03 (Listar materiales), RF-M04 (Tipos de material)

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `dataclass`: Reduce boilerplate para entidades
   - `MaterialType`: Enum para type-safety en tipos de material
   - POR QUÉ separar MaterialType: Single Responsibility Principle

2. **Paso 2 — Definir la clase con dataclass:**
   - `@dataclass(frozen=True)` para inmutabilidad
   - POR QUÉ frozen: Consistencia, thread-safety, cacheability

3. **Paso 2.1 — Campos requeridos:**
   - `id`, `course_id`, `title`, `type`, `url`, `created_at`, `updated_at`
   - POR QUÉ `type: MaterialType`: Usa enum para type-safety

4. **Paso 2.2 — Campos opcionales (específicos de tareas):**
   - `description`, `due_date`, `max_points`
   - POR QUÉ separados: Solo aplican si el material es ASSIGNMENT

5. **Paso 3 — Validaciones en __post_init__:**
   - Validar ID, course_id, title, URL no vacíos
   - Validar URL con formato correcto
   - Validar max_points >= 0
   - Validar due_date >= created_at

6. **Paso 4 — Métodos de negocio:**
   - `is_assignment()`: ¿Es una tarea?
   - `has_due_date()`: ¿Tiene fecha de entrega?
   - `is_overdue()`: ¿Está vencido?
   - `days_until_due()`: Días hasta la entrega
   - `get_type_label()`, `get_type_icon()`: Delegación a MaterialType

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .material_type import MaterialType


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la entidad Material
# ═══════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class Material:
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Campos requeridos
    # ───────────────────────────────────────────────────────────
    id: str
    course_id: str
    title: str
    type: MaterialType  # Enum para type-safety
    url: str
    created_at: datetime
    updated_at: datetime
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.2: Campos opcionales (específicos de tareas)
    # ───────────────────────────────────────────────────────────
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_points: Optional[int] = None
    
    # ───────────────────────────────────────────────────────────
    # Paso 4: Métodos de negocio
    # ───────────────────────────────────────────────────────────
    def is_assignment(self) -> bool:
        return self.type == MaterialType.ASSIGNMENT
    
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.now() > self.due_date
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.domain.entities.material
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: Material
============================================================

1. Crear material válido (PDF):
   ✓ Material creado: Material: Guía de Integrales (PDF)
   ...

✅ Prueba de Material: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ separar Material de Course

| Beneficio | Explicación |
|-----------|-------------|
| **Single Responsibility** | Cada entidad tiene una responsabilidad clara |
| **Reutilizable** | Material puede existir sin Course cargado |
| **Escalable** | Podemos agregar lógica específica de materiales |
| **Testeable** | Podemos testear Material en aislamiento |

### ❌ POR QUÉ NO embeber materiales en Course

| Problema | Ejemplo |
|----------|---------|
| **Acoplamiento** | Cambiar Material requiere cambiar Course |
| **Overhead** | Cargar Course carga todos sus materiales |
| **Complejidad** | Course se vuelve un "god object" |

---

## 🎓 Conceptos Educativos

### Composición vs Herencia

Material NO hereda de Course, sino que tiene una **referencia** (`course_id`):

```python
# ❌ Herencia (incorrecto)
class Material(Course):
    pass

# ✅ Composición (correcto)
class Material:
    course_id: str  # Referencia al curso
```

La composición es más flexible y sigue el principio "Favor composition over inheritance".
