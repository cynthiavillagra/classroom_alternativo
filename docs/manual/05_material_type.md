# 📄 MaterialType (Enum) — Manual Técnico

**Archivo:** `api/domain/entities/material_type.py`  
**Propósito:** Define los tipos de materiales soportados como enumeración type-safe  
**Trazabilidad:** RF-M03 (Tipos de material), Entidad de Dominio

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - Importamos `Enum` de la librería estándar de Python
   - POR QUÉ Enum: Garantiza valores únicos y comparables

2. **Paso 2 — Definir los valores del enum:**
   - Cada tipo tiene un valor string (`"pdf"`, `"video"`, etc.)
   - POR QUÉ minúsculas: Consistencia con APIs REST y JSON

3. **Paso 3 — Agregar métodos helper:**
   - `get_label()`: Etiqueta legible para UI
   - `get_icon()`: Emoji para representación visual
   - `get_color()`: Color hexadecimal para UI
   - POR QUÉ métodos en el enum: Encapsulamos lógica de presentación

4. **Paso 4 — Factory method:**
   - `from_string()`: Convierte string a enum
   - POR QUÉ: Permite crear desde respuestas de API

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema. No reemplaza a los tests unitarios formales.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Enum: Clase base de Python para crear enumeraciones.
# Garantiza que cada valor es único y comparable.
from enum import Enum


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la enumeración de tipos de material
# ═══════════════════════════════════════════════════════════════
class MaterialType(Enum):
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Definir los valores del enum
    # ───────────────────────────────────────────────────────────
    # POR QUÉ valores en minúsculas: Consistencia con APIs REST
    PDF = "pdf"
    VIDEO = "video"
    DOCUMENT = "document"
    LINK = "link"
    FORM = "form"
    IMAGE = "image"
    ASSIGNMENT = "assignment"
    FILE = "file"
    
    # ───────────────────────────────────────────────────────────
    # Paso 3: Métodos helper para UI
    # ───────────────────────────────────────────────────────────
    def get_label(self) -> str:
        """Retorna etiqueta legible para UI."""
        labels = {
            MaterialType.PDF: "PDF",
            MaterialType.VIDEO: "Video",
            # ... más tipos
        }
        return labels.get(self, "Desconocido")
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.domain.entities.material_type
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: MaterialType
============================================================

1. Verificar tipos existentes:
   ✓ PDF = 'pdf'
   ✓ VIDEO = 'video'
   ...

✅ Prueba de MaterialType: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ usar Enum

| Beneficio | Explicación |
|-----------|-------------|
| **Type Safety** | El IDE detecta errores en tiempo de desarrollo |
| **Autocomplete** | Escribes `MaterialType.` y ves todas las opciones |
| **Refactorización** | Cambiar un valor actualiza todos los usos |
| **No typos** | `MaterialType.PDF` vs `"pdff"` (error silencioso) |
| **Documentación** | El código es autodocumentado |

### ❌ POR QUÉ NO usar strings directos

| Problema | Ejemplo |
|----------|---------|
| **Typos** | `"pdf"` vs `"pfd"` - no hay error hasta runtime |
| **Sin autocomplete** | No sabes qué valores son válidos |
| **Difícil buscar** | ¿Dónde se usa `"video"`? Buscar strings es impreciso |
| **Sin validación** | `material_type = "banana"` es válido pero incorrecto |

---

## 🎓 Conceptos Educativos

### ¿Qué es un Enum?
- Conjunto finito de valores constantes con nombre
- Similar a los tipos enumerados de otros lenguajes
- En Python, cada valor es una instancia del enum

### Patrón Rich Enum
Este enum implementa el patrón "Rich Enum" porque tiene:
- Valores (`PDF = "pdf"`)
- Métodos de instancia (`get_label()`, `get_icon()`)
- Factory method (`from_string()`)

Es más que un simple catálogo de constantes.
