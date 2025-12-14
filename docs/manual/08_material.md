# 📖 Material (Entidad) — Manual Técnico

**Archivo:** `api/domain/entities/material.py`  
**Propósito:** Entidad de dominio que representa un material de un curso  
**Trazabilidad:** Entidad de dominio, RF-M03 (Listar materiales), CU-003, HU-003

---

## 📝 Código Clave

```python
from dataclasses import dataclass
from datetime import datetime
from .material_type import MaterialType

@dataclass(frozen=True)
class Material:
    """Entidad inmutable que representa un material."""
    
    id: str
    course_id: str
    title: str
    type: MaterialType
    url: str
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_points: Optional[int] = None
    
    def is_assignment(self) -> bool:
        """Verifica si es una tarea."""
        return self.type == MaterialType.ASSIGNMENT
    
    def is_overdue(self) -> bool:
        """Verifica si está vencido."""
        if not self.has_due_date():
            return False
        return datetime.now() > self.due_date
    
    def days_until_due(self) -> Optional[int]:
        """Días hasta la entrega (negativo si ya pasó)."""
        if not self.has_due_date():
            return None
        delta = self.due_date - datetime.now()
        return delta.days
```

---

## ✅ POR QUÉ SÍ este diseño

| Decisión | Justificación |
|----------|---------------|
| **Métodos de negocio** | `is_overdue()`, `days_until_due()` - Lógica de dominio encapsulada |
| **Validación de URL** | `url.startswith('http')` - Previene URLs inválidas |
| **Campos opcionales** | `due_date`, `max_points` - Solo tareas los tienen |
| **Cálculos en la entidad** | `days_until_due()` - La entidad sabe calcular su estado |

---

## ❌ POR QUÉ NO calcular en el frontend

```python
# ❌ ANTI-PATRÓN: Lógica en el frontend
// JavaScript
const isOverdue = new Date() > new Date(material.due_date);

# ✅ PATRÓN CORRECTO: Lógica en la entidad
material.is_overdue()  # La entidad sabe su estado
```

**POR QUÉ SÍ en la entidad:**
- ✅ **Single Source of Truth**: La lógica está en un solo lugar
- ✅ **Reutilizable**: Cualquier parte del código puede usarla
- ✅ **Testeable**: Fácil de probar con unit tests
- ✅ **Consistente**: Misma lógica en backend y frontend

---

## 🎓 CONCEPTOS EDUCATIVOS

### Rich Domain Model vs. Anemic Domain Model

```python
# ❌ ANEMIC DOMAIN MODEL (anti-patrón)
@dataclass
class Material:
    id: str
    due_date: datetime
    # Solo datos, sin lógica

# Lógica afuera (en un servicio)
def is_overdue(material):
    return datetime.now() > material.due_date

# ✅ RICH DOMAIN MODEL (correcto)
@dataclass
class Material:
    id: str
    due_date: datetime
    
    def is_overdue(self) -> bool:
        """La entidad sabe su lógica."""
        return datetime.now() > self.due_date
```

**POR QUÉ SÍ Rich Domain Model:**
- ✅ Encapsulación: La lógica está donde pertenece
- ✅ Cohesión: Datos y comportamiento juntos
- ✅ Menos acoplamiento: No necesitas servicios externos

### Validación de URLs

```python
def __post_init__(self):
    if not self.url.startswith(('http://', 'https://')):
        raise ValueError(f"URL inválida: {self.url}")

# ✅ Previene:
Material(url="google.com")  # ❌ ValueError
Material(url="ftp://...")   # ❌ ValueError

# ✅ Acepta:
Material(url="https://drive.google.com/...")  # ✅ OK
```

### Campos Opcionales (Optional)

```python
due_date: Optional[datetime] = None
max_points: Optional[int] = None

# POR QUÉ SÍ Optional:
# • No todos los materiales son tareas
# • Un PDF no tiene fecha de entrega
# • Un video no tiene puntos

# Uso seguro:
if material.has_due_date():
    days = material.days_until_due()
```

### Métodos Helper

```python
def has_due_date(self) -> bool:
    """Verifica si tiene fecha de entrega."""
    return self.due_date is not None

# POR QUÉ SÍ este método:
# ✅ Más legible: material.has_due_date()
# ✅ vs: material.due_date is not None
```
