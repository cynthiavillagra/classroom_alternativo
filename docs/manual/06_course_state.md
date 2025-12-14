# 📄 CourseState (Enum) — Manual Técnico

**Archivo:** `api/domain/entities/course_state.py`  
**Propósito:** Define los estados posibles de un curso de Google Classroom  
**Trazabilidad:** RF-M02 (Estados de curso), API de Google Classroom

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - Importamos `Enum` de la librería estándar
   - POR QUÉ: Type-safety y valores constantes garantizados

2. **Paso 2 — Definir valores del enum:**
   - `ACTIVE`, `ARCHIVED`, `PROVISIONED`, `DECLINED`, `SUSPENDED`
   - POR QUÉ MAYÚSCULAS: Así vienen de la API de Google (evitamos conversiones)

3. **Paso 3 — Agregar lógica de negocio:**
   - `is_active()`: ¿El curso está activo?
   - `is_visible()`: ¿Se debe mostrar por defecto?
   - `get_label()`: Etiqueta para UI
   - `get_color()`: Color para representación visual
   - POR QUÉ métodos aquí: Rich Domain Model (encapsulación de reglas)

4. **Paso 4 — Factory method:**
   - `from_string()`: Convierte string de API a enum
   - POR QUÉ: Mapeo seguro desde respuestas JSON

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema. No reemplaza a los tests unitarios formales.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Enum: Type-safety y valores constantes.
from enum import Enum


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la enumeración de estados de curso
# ═══════════════════════════════════════════════════════════════
class CourseState(Enum):
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Valores del enum (estados oficiales de Google)
    # ───────────────────────────────────────────────────────────
    # POR QUÉ MAYÚSCULAS: Así vienen de la API de Google.
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    PROVISIONED = "PROVISIONED"
    DECLINED = "DECLINED"
    SUSPENDED = "SUSPENDED"
    
    # ───────────────────────────────────────────────────────────
    # Paso 3: Métodos de lógica de negocio
    # ───────────────────────────────────────────────────────────
    # POR QUÉ: Rich Domain Model - encapsulamos reglas aquí.
    
    def is_active(self) -> bool:
        """¿El curso está activo?"""
        return self == CourseState.ACTIVE
    
    def is_visible(self) -> bool:
        """¿Se muestra por defecto? (ACTIVE o ARCHIVED)"""
        return self in (CourseState.ACTIVE, CourseState.ARCHIVED)
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.domain.entities.course_state
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: CourseState
============================================================

1. Verificar estados existentes:
   ✓ ACTIVE = 'ACTIVE'
   ✓ ARCHIVED = 'ARCHIVED'
   ...

✅ Prueba de CourseState: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ usar Enum con lógica

| Beneficio | Explicación |
|-----------|-------------|
| **Consistencia con API** | Valores coinciden con Google Classroom API |
| **Lógica encapsulada** | `is_active()` vs `state == "ACTIVE"` |
| **Fácil de extender** | Agregar nuevo estado = agregar valor al enum |
| **Single Source of Truth** | Todo sobre estados en un solo archivo |

### ❌ POR QUÉ NO usar strings o constantes

| Problema | Ejemplo |
|----------|---------|
| **Sin métodos** | No puedes hacer `"ACTIVE".is_visible()` |
| **Dispersión** | Lógica de estados repartida en todo el código |
| **Typos** | `"ACTVE"` vs `"ACTIVE"` - error silencioso |
| **Comparaciones frágiles** | `state.upper() == "ACTIVE"` en todos lados |

---

## 🎓 Conceptos Educativos

### Rich Domain Model vs Anemic Domain Model

**Anemic (❌):** El enum solo tiene valores, la lógica está afuera
```python
# ❌ Anemic
if course.state == "ACTIVE":
    show_course()
```

**Rich (✅):** El enum tiene valores Y comportamiento
```python
# ✅ Rich
if course.state.is_active():
    show_course()
```

El modelo rico es más mantenible y testeable.
