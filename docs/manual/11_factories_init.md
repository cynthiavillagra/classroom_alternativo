# 📦 factories/__init__.py — Manual Técnico

**Archivo:** `api/domain/factories/__init__.py`  
**Propósito:** Convierte la carpeta `factories` en un módulo Python  
**Trazabilidad:** Patrón Factory (docs/02_a), Estructura modular

---

## 📝 Código Completo

```python
"""
Domain Factories Package - Classroom Explorer

Este paquete contiene las factories para crear entidades de dominio.

POR QUÉ SÍ usar Factory Pattern:
✅ Centraliza la creación de entidades complejas
✅ Encapsula validaciones y transformaciones
✅ Facilita crear entidades desde diferentes fuentes (API, tests, etc.)
✅ Permite cambiar la lógica de creación sin afectar el resto del código
"""

from .course_factory import CourseFactory
from .material_factory import MaterialFactory

__all__ = [
    "CourseFactory",
    "MaterialFactory",
]
```

---

## ✅ POR QUÉ SÍ este patrón

| Práctica | Justificación |
|----------|---------------|
| **Docstring extenso** | Explica el propósito del Factory Pattern |
| **`__all__`** | Define qué factories están disponibles |
| **Imports relativos** | `from .course_factory import CourseFactory` |

---

## 🎓 CONCEPTOS EDUCATIVOS

### Estructura de Factories

```
api/domain/factories/
├── __init__.py           ← Este archivo
├── course_factory.py     ← Factory para Course
└── material_factory.py   ← Factory para Material
```

### Uso desde Otros Módulos

```python
# ✅ Import limpio gracias a __init__.py
from api.domain.factories import CourseFactory, MaterialFactory

# Uso:
course = CourseFactory.create_from_dict(api_response)
material = MaterialFactory.create_from_dict(api_response)

# ❌ Sin __init__.py sería:
from api.domain.factories.course_factory import CourseFactory
from api.domain.factories.material_factory import MaterialFactory
# Más verboso
```

### Docstring en __init__.py

```python
"""
Este paquete contiene las factories...

POR QUÉ SÍ usar Factory Pattern:
✅ Centraliza la creación...
"""

# POR QUÉ SÍ docstring extenso:
# ✅ Documenta el propósito del paquete
# ✅ Explica el patrón usado
# ✅ Ayuda a nuevos desarrolladores
# ✅ Aparece en help(api.domain.factories)
```

### Ejemplo Completo

```python
# En infrastructure/mappers/classroom_mapper.py
from api.domain.factories import CourseFactory, MaterialFactory

class ClassroomMapper:
    def api_course_to_domain(self, api_data: dict) -> Course:
        """Convierte respuesta de API a entidad."""
        return CourseFactory.create_from_dict(api_data)
    
    def api_material_to_domain(self, api_data: dict) -> Material:
        """Convierte respuesta de API a entidad."""
        return MaterialFactory.create_from_dict(api_data)
```
