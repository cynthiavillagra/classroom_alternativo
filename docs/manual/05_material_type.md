# 🔢 MaterialType (Enum) — Manual Técnico

**Archivo:** `api/domain/entities/material_type.py`  
**Propósito:** Define los tipos de materiales soportados  
**Trazabilidad:** Entidad de dominio, RF-M03 (Listar materiales)

---

## 📝 Código Completo

```python
from enum import Enum

class MaterialType(Enum):
    """Tipos de materiales soportados."""
    
    PDF = "pdf"
    VIDEO = "video"
    DOCUMENT = "document"
    LINK = "link"
    FORM = "form"
    IMAGE = "image"
    ASSIGNMENT = "assignment"
    FILE = "file"
    
    def get_label(self) -> str:
        """Retorna la etiqueta legible para UI."""
        labels = {
            MaterialType.PDF: "PDF",
            MaterialType.VIDEO: "Video",
            MaterialType.DOCUMENT: "Documento",
            MaterialType.LINK: "Enlace",
            MaterialType.FORM: "Formulario",
            MaterialType.IMAGE: "Imagen",
            MaterialType.ASSIGNMENT: "Tarea",
            MaterialType.FILE: "Archivo"
        }
        return labels.get(self, "Desconocido")
    
    def get_icon(self) -> str:
        """Retorna el emoji/icono asociado."""
        icons = {
            MaterialType.PDF: "📄",
            MaterialType.VIDEO: "🎥",
            MaterialType.DOCUMENT: "📝",
            MaterialType.LINK: "🔗",
            MaterialType.FORM: "📋",
            MaterialType.IMAGE: "🖼️",
            MaterialType.ASSIGNMENT: "✏️",
            MaterialType.FILE: "📎"
        }
        return icons.get(self, "📎")
    
    def get_color(self) -> str:
        """Retorna el color sugerido para UI (hex)."""
        colors = {
            MaterialType.PDF: "#E74C3C",        # Rojo
            MaterialType.VIDEO: "#9B59B6",      # Púrpura
            MaterialType.DOCUMENT: "#3498DB",   # Azul
            MaterialType.LINK: "#1ABC9C",       # Turquesa
            MaterialType.FORM: "#F39C12",       # Naranja
            MaterialType.IMAGE: "#E67E22",      # Naranja oscuro
            MaterialType.ASSIGNMENT: "#2ECC71", # Verde
            MaterialType.FILE: "#95A5A6"        # Gris
        }
        return colors.get(self, "#95A5A6")
```

---

## ✅ POR QUÉ SÍ usar Enum

- ✅ Evita strings mágicos ("pdf", "video", etc.)
- ✅ Autocomplete en el IDE
- ✅ Type safety (el IDE detecta errores)
- ✅ Fácil de extender (agregar nuevos tipos)
- ✅ Métodos helper (`get_label()`, `get_icon()`)

---

## ❌ POR QUÉ NO usar strings directamente

```python
# ❌ ANTI-PATRÓN: Strings mágicos
material_type = "pdf"  # Typo: "pfd" no se detecta
if material_type == "video":  # Repetitivo, propenso a errores
    ...

# ✅ PATRÓN CORRECTO: Enum
material_type = MaterialType.PDF
if material_type == MaterialType.VIDEO:  # Autocomplete, type-safe
    ...
```

**Problemas de strings:**
- ❌ Typos no se detectan hasta runtime
- ❌ No hay autocomplete
- ❌ Difícil de refactorizar
- ❌ No hay validación de tipos

---

## 🎓 CONCEPTOS EDUCATIVOS

### ¿Qué es un Enum?

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Uso:
color = Color.RED
print(color.value)  # 1
print(color.name)   # "RED"
```

**Beneficios:**
- ✅ Conjunto fijo de valores
- ✅ Type-safe
- ✅ Autocomplete en IDE
- ✅ Puede tener métodos

### Métodos en Enums

```python
class MaterialType(Enum):
    PDF = "pdf"
    
    def get_label(self) -> str:
        """Método personalizado."""
        return "PDF Document"

# Uso:
type = MaterialType.PDF
print(type.get_label())  # "PDF Document"
```

**POR QUÉ SÍ métodos en enums:**
- ✅ Encapsula lógica relacionada
- ✅ Evita funciones sueltas
- ✅ Más orientado a objetos

### Enum vs. Constantes

```python
# ❌ CONSTANTES (anti-patrón)
PDF = "pdf"
VIDEO = "video"
DOCUMENT = "document"

# Problema: No hay agrupación, no hay validación

# ✅ ENUM (correcto)
class MaterialType(Enum):
    PDF = "pdf"
    VIDEO = "video"
    DOCUMENT = "document"

# Beneficio: Agrupado, validado, type-safe
```

### Conversión desde String

```python
@classmethod
def from_string(cls, value: str) -> 'MaterialType':
    """Crea desde un string."""
    try:
        return cls(value.lower())
    except ValueError:
        raise ValueError(f"Tipo inválido: '{value}'")

# Uso:
type = MaterialType.from_string("PDF")  # MaterialType.PDF
type = MaterialType.from_string("invalid")  # ValueError
```
