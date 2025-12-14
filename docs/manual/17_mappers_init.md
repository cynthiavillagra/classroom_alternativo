# 📄 Mappers __init__.py — Manual Técnico

**Archivo:** `api/infrastructure/mappers/__init__.py`  
**Propósito:** Exportar el ClassroomMapper  
**Trazabilidad:** Clean Architecture, Package Structure

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Import de ClassroomMapper:** El único mapper por ahora
2. **Paso 2 — __all__:** Lista explícita de exports públicos

---

## 📝 Contenido Actual

```python
from .classroom_mapper import ClassroomMapper

__all__ = [
    "ClassroomMapper",
]
```

---

## 🎓 Aclaración Metodológica

Este archivo es un `__init__.py` que solo hace exports. No tiene lógica propia, por lo que no requiere prueba atómica.

---

## 🔥 Prueba de Fuego

### Verificación de imports
```powershell
python -c "from api.infrastructure.mappers import ClassroomMapper; print('✅ Mapper exportado correctamente')"
```

### Salida Esperada
```
✅ Mapper exportado correctamente
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ carpeta mappers separada

| Beneficio | Explicación |
|-----------|-------------|
| **Escalabilidad** | Podremos agregar más mappers |
| **Organización** | Cada mapper en su archivo |
| **Single Responsibility** | Mapper solo convierte formatos |

### ❌ POR QUÉ NO poner mapper en el repositorio

| Problema | Impacto |
|----------|---------|
| **Violación SRP** | Repositorio haría HTTP + conversión |
| **Difícil de testear** | Mezcla responsabilidades |
| **No reutilizable** | Otro repo no podría usar el mapper |
