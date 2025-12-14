# 📄 ClassroomRepository (Interface) — Manual Técnico

**Archivo:** `api/domain/interfaces/classroom_repository.py`  
**Propósito:** Interface (Port) que define contrato para acceder a datos  
**Trazabilidad:** Hexagonal Architecture, Dependency Inversion Principle

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `ABC`: Abstract Base Class de Python
   - `abstractmethod`: Decorador que fuerza implementación
   - POR QUÉ ABC: Estándar de Python para interfaces

2. **Paso 2 — Definir la clase abstracta:**
   - Hereda de `ABC`
   - Define QUÉ operaciones existen, no CÓMO
   - POR QUÉ Hexagonal: Dominio define contratos, infra implementa

3. **Paso 2.1 — Métodos abstractos:**
   - `get_user_courses()`: Lista cursos de un usuario
   - `get_course_materials()`: Lista materiales de un curso
   - `get_course_by_id()`: Obtiene un curso específico
   - POR QUÉ abstractmethod: Fuerza que subclases implementen

4. **Paso 3 — Excepciones personalizadas:**
   - `RepositoryError`: Error base del repositorio
   - `CourseNotFoundError`: Curso no encontrado
   - `MaterialNotFoundError`: Material no encontrado
   - `UnauthorizedError`: Token inválido
   - POR QUÉ excepciones propias: Desacoplamos de errores de Google

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque verifica que la interface está bien definida y que las excepciones funcionan. NO hace llamadas reales porque es una INTERFACE sin implementación.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ ABC: Abstract Base Class para definir interfaces
from abc import ABC, abstractmethod
from typing import List
from ..entities.course import Course
from ..entities.material import Material


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la interface (Port)
# ═══════════════════════════════════════════════════════════════
class ClassroomRepository(ABC):
    """Interface que define contrato para acceso a datos."""
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Métodos abstractos (contrato)
    # ───────────────────────────────────────────────────────────
    @abstractmethod
    def get_user_courses(self, user_id: str, access_token: str) -> List[Course]:
        """Lista cursos de un usuario."""
        pass
    
    @abstractmethod
    def get_course_materials(self, course_id: str, access_token: str) -> List[Material]:
        """Lista materiales de un curso."""
        pass


# ═══════════════════════════════════════════════════════════════
# Paso 3: Excepciones del repositorio
# ═══════════════════════════════════════════════════════════════
class RepositoryError(Exception):
    """Error base del repositorio."""
    pass

class CourseNotFoundError(RepositoryError):
    """Curso no encontrado."""
    pass
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.domain.interfaces.classroom_repository
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: ClassroomRepository
============================================================

1. Verificar que es abstracta:
   ✓ No se puede instanciar directamente
   ...

✅ Prueba de ClassroomRepository: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ usar Interface (Port)

| Beneficio | Explicación |
|-----------|-------------|
| **Hexagonal Architecture** | Dominio define contrato, infra implementa |
| **Dependency Inversion** | El dominio no depende de Google API |
| **Testing fácil** | Podemos crear MockRepository para tests |
| **Flexibilidad** | Cambiar de Google a otro proveedor es fácil |

### ❌ POR QUÉ NO depender directamente de Google API

| Problema | Impacto |
|----------|---------|
| **Acoplamiento** | Dominio atado a Google |
| **Testing difícil** | Hay que llamar a Google en tests |
| **Inflexible** | Cambiar proveedor requiere cambiar dominio |
| **Violación DIP** | Alto nivel depende de bajo nivel |

---

## 🎓 Conceptos Educativos

### Dependency Inversion Principle (DIP)

**Antes (❌ violando DIP):**
```
UseCase → GoogleClassroomClient (acoplamiento directo)
```

**Después (✅ con interface):**
```
UseCase → ClassroomRepository (interface)
                    ↑
        GoogleClassroomRepository (implementación)
```

El dominio depende de una abstracción, no de detalles.

### Port en Hexagonal Architecture

La interface es un "puerto" por donde el dominio puede recibir datos:
- El dominio define QUÉ necesita (interface)
- La infraestructura define CÓMO lo provee (implementación)
