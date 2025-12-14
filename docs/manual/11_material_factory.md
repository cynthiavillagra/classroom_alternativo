# 📄 MaterialFactory — Manual Técnico

**Archivo:** `api/domain/factories/material_factory.py`  
**Propósito:** Factory Pattern para crear instancias válidas de Material  
**Trazabilidad:** Patrón Factory, Creación de materiales desde API

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `Material`: La entidad que vamos a crear
   - `MaterialType`: Enum para tipos de material
   - POR QUÉ: Type-safety y centralización

2. **Paso 2 — Definir la clase Factory:**
   - POR QUÉ similar a CourseFactory: Consistencia en patrones
   - Misma estructura: `create()`, `create_from_dict()`, `create_for_testing()`

3. **Paso 2.1 — Método `create()` (creación directa):**
   - Normaliza title, description, URL
   - Convierte description vacío a None
   - POR QUÉ normalizar: Consistencia en datos

4. **Paso 2.2 — Método `create_from_dict()` (desde API):**
   - Valida campos obligatorios
   - Convierte string → MaterialType
   - Convierte string → datetime
   - POR QUÉ: Respuestas de Google API vienen como dict

5. **Paso 2.3 — Método `create_for_testing()`:**
   - Valores por defecto sensatos (PDF, URL válida)
   - Acepta **kwargs para override
   - POR QUÉ: Testing simple y flexible

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
from datetime import datetime
from typing import Dict, Any, Optional
from ..entities.material import Material
from ..entities.material_type import MaterialType


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la clase Factory
# ═══════════════════════════════════════════════════════════════
class MaterialFactory:
    
    @staticmethod
    def create(id, course_id, title, type, url, ...) -> Material:
        # Normalizar strings
        title = title.strip() if title else ""
        description = description.strip() if description else None
        if description == "":
            description = None
        return Material(...)
    
    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> Material:
        # Validar campos obligatorios
        required_fields = ['id', 'course_id', 'title', 'type', 'url']
        # Convertir type string → enum
        material_type = MaterialType.from_string(data['type'])
        # Convertir fechas
        created_at = datetime.fromisoformat(data['created_at'])
        return MaterialFactory.create(...)
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.domain.factories.material_factory
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: MaterialFactory
============================================================

1. MaterialFactory.create():
   ✓ Material creado: Material: Guía de Integrales (PDF)
   ...

✅ Prueba de MaterialFactory: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ Factory consistente con CourseFactory

| Beneficio | Explicación |
|-----------|-------------|
| **Consistencia** | Mismo patrón para Course y Material |
| **Curva de aprendizaje** | Quien conoce CourseFactory entiende MaterialFactory |
| **Mantenibilidad** | Cambios en el patrón se aplican a ambos |
| **Testing** | `create_for_testing()` simplifica tests |

### ❌ POR QUÉ NO crear directamente Material()

| Problema | Ejemplo |
|----------|---------|
| **Sin normalización** | `"  Video Tutorial  "` queda con espacios |
| **Sin conversión** | `type="pdf"` falla (necesita `MaterialType.PDF`) |
| **Fechas complicadas** | ISO strings requieren conversión manual |
| **Testing verboso** | Hay que especificar todos los campos |

---

## 🎓 Conceptos Educativos

### Consistencia en Patrones

Mantener el mismo patrón para entidades similares:

```python
# ✅ Consistente
course = CourseFactory.create_from_dict(course_data)
material = MaterialFactory.create_from_dict(material_data)

# ✅ Testing consistente
test_course = CourseFactory.create_for_testing()
test_material = MaterialFactory.create_for_testing()
```

### Normalización de Datos

El factory limpia los datos antes de crear la entidad:
- Espacios en blanco: `"  Hello  "` → `"Hello"`
- Strings vacíos: `""` → `None`
- Tipos: `"pdf"` → `MaterialType.PDF`
