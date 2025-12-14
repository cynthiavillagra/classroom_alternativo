# 📦 entities/__init__.py — Manual Técnico

**Archivo:** `api/domain/entities/__init__.py`  
**Propósito:** Convierte la carpeta `entities` en un módulo Python  
**Trazabilidad:** RNF-MANT04 (Convenciones de código), Estructura modular

---

## 📝 Código Completo

```python
"""
Domain Entities Package - Classroom Explorer

Este paquete contiene las entidades de dominio del sistema.
"""

from .course import Course
from .material import Material
from .material_type import MaterialType
from .course_state import CourseState

__all__ = [
    "Course",
    "Material",
    "MaterialType",
    "CourseState",
]
```

---

## ✅ POR QUÉ SÍ este patrón

| Práctica | Justificación |
|----------|---------------|
| **`__all__`** | Define qué se exporta con `from entities import *` |
| **Imports relativos** | `from .course import Course` (más limpio) |
| **Documentación** | Docstring explica el propósito del paquete |
| **Centralización** | Un solo lugar para ver todas las entidades |

---

## ❌ POR QUÉ NO dejarlo vacío

```python
# ❌ SIN __init__.py con exports
from api.domain.entities.course import Course
from api.domain.entities.material import Material
from api.domain.entities.material_type import MaterialType

# ✅ CON __init__.py con exports
from api.domain.entities import Course, Material, MaterialType
```

**Beneficios:**
- ✅ Imports más cortos y legibles
- ✅ Documentación implícita de la API pública
- ✅ Fácil de refactorizar (cambiar ubicación interna)

---

## 🎓 CONCEPTOS EDUCATIVOS

### ¿Qué es `__init__.py`?

- Archivo especial que Python busca para reconocer un paquete
- Se ejecuta cuando importas el paquete
- Puede estar vacío o contener código de inicialización

```python
# Estructura:
api/
└── domain/
    └── entities/
        ├── __init__.py      ← Este archivo
        ├── course.py
        ├── material.py
        └── material_type.py

# Sin __init__.py:
# Python 3.3+ lo permite (namespace packages)
# Pero es menos explícito

# Con __init__.py:
# Python reconoce explícitamente como paquete
# Puedes controlar qué se exporta
```

### ¿Qué es `__all__`?

```python
__all__ = ["Course", "Material"]

# Controla qué se exporta con:
from api.domain.entities import *

# Solo exporta Course y Material
# Otras clases/funciones quedan privadas
```

**POR QUÉ SÍ usar `__all__`:**
- ✅ Documentación explícita de la API pública
- ✅ Evita exportar funciones/clases internas
- ✅ IDEs usan esta info para autocomplete

**POR QUÉ NO abusar de `import *`:**
- ❌ No sabes qué estás importando
- ❌ Puede causar conflictos de nombres
- ✅ **Mejor:** Imports explícitos

### Imports Relativos vs. Absolutos

```python
# IMPORTS RELATIVOS (en __init__.py)
from .course import Course
from .material import Material

# IMPORTS ABSOLUTOS
from api.domain.entities.course import Course
from api.domain.entities.material import Material

# POR QUÉ SÍ relativos en __init__.py:
# ✅ Más cortos
# ✅ Fácil de mover el paquete
# ✅ No depende de la ruta absoluta
```

### Ejemplo de Uso

```python
# En otro archivo:
from api.domain.entities import Course, Material, MaterialType

# Crear instancias:
course = Course(...)
material = Material(type=MaterialType.PDF, ...)

# Sin __init__.py sería:
from api.domain.entities.course import Course
from api.domain.entities.material import Material
from api.domain.entities.material_type import MaterialType
# Más verboso
```
