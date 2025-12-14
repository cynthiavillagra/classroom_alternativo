# 📄 CourseFactory — Manual Técnico

**Archivo:** `api/domain/factories/course_factory.py`  
**Propósito:** Factory Pattern para crear instancias válidas de Course  
**Trazabilidad:** Patrón Factory, Creación de entidades desde API

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `Course`: La entidad que vamos a crear
   - `CourseState`: Enum para estados válidos
   - POR QUÉ imports separados: Claridad y mantenibilidad

2. **Paso 2 — Definir la clase Factory:**
   - POR QUÉ Factory Pattern: Centraliza creación, valida, transforma
   - POR QUÉ @staticmethod: No necesita estado de instancia

3. **Paso 2.1 — Método `create()` (creación directa):**
   - Recibe parámetros tipados
   - Normaliza strings (strip)
   - Convierte None a valores vacíos
   - POR QUÉ normalizar: Datos limpios desde el inicio

4. **Paso 2.2 — Método `create_from_dict()` (desde API):**
   - Valida campos obligatorios
   - Convierte tipos (string → enum, string → datetime)
   - POR QUÉ separar: Respuestas de API vienen como dict

5. **Paso 2.3 — Método `create_for_testing()`:**
   - Valores por defecto sensatos
   - Fácil de usar en tests
   - POR QUÉ: Evita duplicar setup en cada test

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
from typing import Dict, Any
from ..entities.course import Course
from ..entities.course_state import CourseState


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la clase Factory
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Factory Pattern: Centraliza creación, valida, transforma.
class CourseFactory:
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Método create() - Creación directa
    # ───────────────────────────────────────────────────────────
    @staticmethod
    def create(id: str, name: str, state: CourseState, ...) -> Course:
        # Normalizar strings
        name = name.strip() if name else ""
        # Crear entidad
        return Course(id=id, name=name, ...)
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.2: Método create_from_dict() - Desde API response
    # ───────────────────────────────────────────────────────────
    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> Course:
        # Validar campos obligatorios
        required = ['id', 'name', 'state', 'ownerId']
        # Convertir tipos
        state = CourseState.from_string(data['state'])
        # Crear usando create()
        return CourseFactory.create(...)
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.domain.factories.course_factory
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: CourseFactory
============================================================

1. CourseFactory.create():
   ✓ Curso creado: Course: Matemáticas 3°A - Turno Mañana (ACTIVE)
   ...

✅ Prueba de CourseFactory: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ usar Factory Pattern

| Beneficio | Explicación |
|-----------|-------------|
| **Centralización** | Toda la lógica de creación en un lugar |
| **Validación previa** | Valida antes de crear (fail-fast) |
| **Transformación** | Convierte tipos (string → enum, string → datetime) |
| **Múltiples fuentes** | `create()`, `create_from_dict()`, `create_for_testing()` |
| **Testeable** | Fácil de mockear en tests |

### ❌ POR QUÉ NO crear directamente con Course()

| Problema | Ejemplo |
|----------|---------|
| **Sin normalización** | Espacios en blanco no se limpian |
| **Sin conversión** | `state="ACTIVE"` falla (necesita enum) |
| **Repetición** | Misma lógica de conversión en muchos lugares |
| **Testing difícil** | Hay que crear todos los parámetros cada vez |

---

## 🎓 Conceptos Educativos

### Factory Pattern

El patrón Factory encapsula la lógica de creación de objetos:

```python
# ❌ Sin Factory (repetitivo, propenso a errores)
course = Course(
    id="123",
    name="Math  ",  # Espacios no limpiados
    state=CourseState.from_string("ACTIVE"),  # Conversión manual
    created_at=datetime.fromisoformat("2024-01-15T10:00:00Z".replace('Z', '+00:00')),
    ...
)

# ✅ Con Factory (limpio, validado)
course = CourseFactory.create_from_dict(api_response)
```

### Static Methods

Usamos `@staticmethod` porque:
- No necesitamos acceso a `self`
- No mantenemos estado
- Es puramente funcional
