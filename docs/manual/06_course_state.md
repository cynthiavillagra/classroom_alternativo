# 🔢 CourseState (Enum) — Manual Técnico

**Archivo:** `api/domain/entities/course_state.py`  
**Propósito:** Define los estados de un curso en Google Classroom  
**Trazabilidad:** Entidad de dominio, RF-M02 (Listar cursos)

---

## 📝 Código Completo

```python
from enum import Enum

class CourseState(Enum):
    """Estados de un curso en Google Classroom."""
    
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    PROVISIONED = "PROVISIONED"
    DECLINED = "DECLINED"
    SUSPENDED = "SUSPENDED"
    
    def is_active(self) -> bool:
        """Verifica si el curso está activo."""
        return self == CourseState.ACTIVE
    
    def is_visible(self) -> bool:
        """Verifica si el curso debería mostrarse por defecto."""
        return self in (CourseState.ACTIVE, CourseState.ARCHIVED)
    
    def get_label(self) -> str:
        """Retorna la etiqueta legible para UI."""
        labels = {
            CourseState.ACTIVE: "Activo",
            CourseState.ARCHIVED: "Archivado",
            CourseState.PROVISIONED: "Pendiente",
            CourseState.DECLINED: "Rechazado",
            CourseState.SUSPENDED: "Suspendido"
        }
        return labels.get(self, "Desconocido")
    
    def get_color(self) -> str:
        """Retorna el color sugerido para UI."""
        colors = {
            CourseState.ACTIVE: "#2ECC71",      # Verde
            CourseState.ARCHIVED: "#95A5A6",    # Gris
            CourseState.PROVISIONED: "#F39C12", # Naranja
            CourseState.DECLINED: "#E74C3C",    # Rojo
            CourseState.SUSPENDED: "#E67E22"    # Naranja oscuro
        }
        return colors.get(self, "#95A5A6")
```

---

## ✅ POR QUÉ SÍ este diseño

| Decisión | Justificación |
|----------|---------------|
| **Enum** | Valores fijos definidos por Google Classroom API |
| **Métodos helper** | `is_active()`, `is_visible()` - Lógica de negocio |
| **get_label()** | Traducción a español para UI |
| **get_color()** | Colores consistentes en toda la app |

---

## 🎓 CONCEPTOS EDUCATIVOS

### Estados oficiales de Google Classroom API

Basado en la documentación oficial:
https://developers.google.com/classroom/reference/rest/v1/courses#CourseState

| Estado | Descripción | Cuándo Ocurre |
|--------|-------------|---------------|
| **ACTIVE** | Curso activo y visible | Estado normal de un curso |
| **ARCHIVED** | Curso archivado (solo lectura) | Profesor archiva el curso |
| **PROVISIONED** | Curso creado pero no activado | Curso recién creado |
| **DECLINED** | Invitación rechazada | Usuario rechaza invitación |
| **SUSPENDED** | Curso suspendido | Administrador suspende el curso |

### Métodos de Negocio en Enums

```python
def is_visible(self) -> bool:
    """Cursos que se muestran en la UI."""
    return self in (CourseState.ACTIVE, CourseState.ARCHIVED)

# POR QUÉ SÍ este método:
# ✅ Encapsula lógica de negocio
# ✅ Evita repetir la condición en muchos lugares
# ✅ Fácil de cambiar (ej: agregar PROVISIONED)

# Uso:
if course.state.is_visible():
    display(course)
```

### Conversión desde String

```python
@classmethod
def from_string(cls, value: str) -> 'CourseState':
    """Crea desde un string (API response)."""
    try:
        return cls(value.upper())
    except ValueError:
        raise ValueError(
            f"Estado inválido: '{value}'. "
            f"Estados válidos: {', '.join([s.value for s in cls])}"
        )

# Uso:
state = CourseState.from_string("active")  # CourseState.ACTIVE
state = CourseState.from_string("ACTIVE")  # CourseState.ACTIVE
state = CourseState.from_string("invalid") # ValueError con mensaje claro
```

**POR QUÉ SÍ validar:**
- ✅ Fail-fast: detecta errores inmediatamente
- ✅ Mensaje claro: lista los valores válidos
- ✅ Case-insensitive: acepta "active" y "ACTIVE"
