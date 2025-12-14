# 📄 ClassroomMapper — Manual Técnico

**Archivo:** `api/infrastructure/mappers/classroom_mapper.py`  
**Propósito:** Adapter Pattern para convertir respuestas de Google API a entidades  
**Trazabilidad:** Hexagonal Architecture, Adapter Pattern

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `datetime`: Para parsear timestamps de Google
   - `Factories`: Para crear entidades válidas
   - POR QUÉ factories: Reutilizamos lógica de validación

2. **Paso 2 — Definir la clase Mapper:**
   - Único lugar que conoce estructura de Google API
   - POR QUÉ Adapter: Aísla cambios de API externa

3. **Paso 2.1 — Método `api_course_to_domain()`:**
   - Extrae campos del JSON de Google
   - Convierte `state` string → CourseState enum
   - Parsea timestamps ISO → datetime
   - POR QUÉ: Google usa camelCase, nosotros snake_case

4. **Paso 2.2 — Método `api_material_to_domain()`:**
   - Detecta tipo de material (PDF, video, etc.)
   - Extrae URL del material
   - Parsea due_date si existe
   - POR QUÉ: La estructura de materiales es compleja

5. **Paso 3 — Métodos helper privados:**
   - `_detect_material_type()`: Detecta tipo por extensión/URL
   - `_extract_material_url()`: Extrae URL de diferentes estructuras
   - `_parse_google_timestamp()`: Parsea formato ISO de Google
   - `_parse_due_date()`: Parsea fecha de entrega
   - POR QUÉ privados: Lógica interna, no exponer

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento usando datos mock de API, sin llamar a Google.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from api.domain.entities import Course, Material, MaterialType, CourseState
from api.domain.factories import CourseFactory, MaterialFactory


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir el Mapper (Adapter Pattern)
# ═══════════════════════════════════════════════════════════════
class ClassroomMapper:
    """ÚNICO lugar que conoce la estructura de Google API."""
    
    def api_course_to_domain(self, api_data: Dict[str, Any]) -> Course:
        # Paso 2.1.1: Extraer campos de la respuesta de Google
        id = api_data['id']
        name = api_data['name']
        state = CourseState.from_string(api_data.get('courseState', 'ACTIVE'))
        
        # Paso 2.1.2: Parsear timestamps
        created_at = self._parse_google_timestamp(api_data['creationTime'])
        
        # Paso 2.1.3: Usar factory para crear entidad válida
        return CourseFactory.create(id=id, name=name, ...)
    
    def _detect_material_type(self, api_data: Dict) -> MaterialType:
        # Paso 3.1: Detectar por extensión o tipo de contenido
        if 'driveFile' in api_data.get('materials', [{}])[0]:
            # Es archivo de Drive, detectar por extensión
            ...
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.infrastructure.mappers.classroom_mapper
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: ClassroomMapper
============================================================

1. Convertir curso de API a dominio:
   ✓ Curso: Matemáticas 3°A (ACTIVE)
   ...

✅ Prueba de ClassroomMapper: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ usar Mapper (Adapter Pattern)

| Beneficio | Explicación |
|-----------|-------------|
| **Aislamiento** | Cambios en Google API = cambios solo aquí |
| **Single Responsibility** | Mapper solo convierte, no hace HTTP |
| **Testeable** | Podemos testear con mock API data |
| **Dominio limpio** | El dominio no sabe nada de Google |

### ❌ POR QUÉ NO convertir directamente en el repositorio

| Problema | Impacto |
|----------|---------|
| **Mezcla de responsabilidades** | HTTP + conversión en un archivo |
| **Difícil de testear** | Hay que mockear HTTP para testear conversión |
| **Cambios riesgosos** | Tocar conversión puede romper HTTP |

---

## 🎓 Conceptos Educativos

### Adapter Pattern

El Adapter convierte una interfaz en otra:

```
Google API Response (camelCase)     →     Domain Entity (snake_case)
{                                          Course(
  "id": "123",                               id="123",
  "ownerId": "456",                          owner_id="456",
  "courseState": "ACTIVE"                    state=CourseState.ACTIVE
}                                          )
```

### Single Responsibility Principle

- **Mapper**: Solo convierte formatos
- **Repository**: Solo hace HTTP
- **Factory**: Solo crea entidades válidas

Cada clase tiene UNA razón para cambiar.
