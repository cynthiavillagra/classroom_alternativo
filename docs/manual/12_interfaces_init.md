# 📄 Interfaces __init__.py — Manual Técnico

**Archivo:** `api/domain/interfaces/__init__.py`  
**Propósito:** Exportar interfaces y excepciones del dominio  
**Trazabilidad:** Clean Architecture, Package Structure

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Import de ClassroomRepository:** La interface principal
2. **Paso 2 — Import de excepciones:** RepositoryError, CourseNotFoundError, etc.
3. **Paso 3 — __all__:** Lista explícita de exports públicos

---

## 📝 Contenido Actual

```python
from .classroom_repository import (
    ClassroomRepository,
    RepositoryError,
    CourseNotFoundError,
    MaterialNotFoundError,
    UnauthorizedError
)

__all__ = [
    "ClassroomRepository",
    "RepositoryError",
    "CourseNotFoundError",
    "MaterialNotFoundError",
    "UnauthorizedError",
]
```

---

## 🎓 Aclaración Metodológica

Este archivo es un `__init__.py` que solo hace exports. No tiene lógica propia, por lo que no requiere prueba atómica con `if __name__ == "__main__"`.

---

## 🔥 Prueba de Fuego

### Verificación de imports
```powershell
python -c "from api.domain.interfaces import ClassroomRepository, RepositoryError; print('✅ Interfaces exportadas correctamente')"
```

### Salida Esperada
```
✅ Interfaces exportadas correctamente
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ exports explícitos

| Beneficio | Explicación |
|-----------|-------------|
| **Imports limpios** | `from api.domain.interfaces import X` |
| **API pública clara** | `__all__` define qué es público |
| **Encapsulación** | Oculta detalles internos |

### ❌ POR QUÉ NO sin __init__.py

| Problema | Impacto |
|----------|---------|
| **Imports largos** | `from api.domain.interfaces.classroom_repository import X` |
| **Sin control** | Todo es público por defecto |
