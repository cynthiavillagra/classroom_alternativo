# 📚 Course (Entidad) — Manual Técnico

**Archivo:** `api/domain/entities/course.py`  
**Propósito:** Entidad de dominio que representa un curso de Google Classroom  
**Trazabilidad:** Entidad de dominio, RF-M02 (Listar cursos), CU-002, HU-002

---

## 📝 Código Clave

```python
from dataclasses import dataclass
from datetime import datetime
from .course_state import CourseState

@dataclass(frozen=True)
class Course:
    """Entidad inmutable que representa un curso."""
    
    id: str
    name: str
    state: CourseState
    owner_id: str
    created_at: datetime
    updated_at: datetime
    section: Optional[str] = None
    description: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones automáticas."""
        if not self.id or not self.id.strip():
            raise ValueError("Course ID no puede estar vacío")
        
        if len(self.name.strip()) < 3:
            raise ValueError("Course name debe tener al menos 3 caracteres")
    
    def is_active(self) -> bool:
        """Verifica si el curso está activo."""
        return self.state.is_active()
    
    def to_dict(self) -> dict:
        """Serializa a diccionario para JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state.value,
            'created_at': self.created_at.isoformat()
        }
```

---

## ✅ POR QUÉ SÍ este diseño

| Decisión | Justificación |
|----------|---------------|
| **`@dataclass`** | Menos boilerplate, genera `__init__`, `__repr__`, `__eq__` automáticamente |
| **`frozen=True`** | Inmutabilidad: una vez creado, no se puede modificar |
| **`__post_init__`** | Validaciones automáticas al crear la instancia |
| **Type hints** | `id: str`, `state: CourseState` - El IDE detecta errores |
| **Métodos de negocio** | `is_active()`, `is_visible()` - Lógica de dominio encapsulada |
| **`to_dict()`** | Serialización controlada para JSON |

---

## ❌ POR QUÉ NO otras alternativas

| Alternativa | Por Qué NO |
|-------------|------------|
| **Clase normal** | Más código (necesitas escribir `__init__`, `__repr__`, etc.) |
| **Diccionario** | No hay validación, no hay autocomplete, propenso a errores |
| **Mutable** | Permite modificaciones accidentales, bugs difíciles de rastrear |
| **Pydantic** | Más pesado, innecesario para entidades de dominio puras |

---

## 🎓 CONCEPTOS EDUCATIVOS

### ¿Qué es una Entidad de Dominio?
- Representa un concepto del negocio (Course, Material, etc.)
- Tiene identidad única (`id`)
- Contiene lógica de negocio (`is_active()`)
- **NO** conoce detalles de infraestructura (HTTP, DB, etc.)

### ¿Por qué Inmutabilidad (frozen=True)?

```python
# ❌ SIN frozen=True (mutable)
course = Course(id="123", name="Math")
course.name = "History"  # ¡Modificación accidental!
# Bug difícil de rastrear

# ✅ CON frozen=True (inmutable)
course = Course(id="123", name="Math")
course.name = "History"  # ❌ Error: FrozenInstanceError
# El error se detecta inmediatamente
```

**Beneficios:**
- ✅ **Thread-safe**: Seguro en concurrencia
- ✅ **Predecible**: El estado no cambia inesperadamente
- ✅ **Cacheable**: Puede usarse como key en diccionarios
- ✅ **Menos bugs**: No hay modificaciones accidentales

### ¿Qué es `__post_init__`?
- Método especial de `dataclass`
- Se ejecuta **después** de `__init__`
- Ideal para validaciones

```python
@dataclass(frozen=True)
class Course:
    name: str
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Name is required")

# ✅ Válido
course = Course(name="Math")

# ❌ Error inmediato
course = Course(name="")  # ValueError: Name is required
```
