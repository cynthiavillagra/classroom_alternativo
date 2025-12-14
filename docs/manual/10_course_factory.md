# 🏭 CourseFactory — Manual Técnico

**Archivo:** `api/domain/factories/course_factory.py`  
**Propósito:** Factory para crear instancias de Course con validaciones y transformaciones  
**Trazabilidad:** Patrón Factory (docs/02_a), Creación de entidades

---

## 📝 Código Clave

```python
class CourseFactory:
    """Factory para crear instancias de Course."""
    
    @staticmethod
    def create(
        id: str,
        name: str,
        state: CourseState,
        owner_id: str,
        created_at: datetime,
        updated_at: datetime,
        section: str = None,
        description: str = None
    ) -> Course:
        """Crea una instancia de Course con validaciones."""
        # Normalizar datos
        name = name.strip() if name else ""
        section = section.strip() if section else None
        
        # Crear entidad
        return Course(id=id, name=name, state=state, ...)
    
    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> Course:
        """Crea desde un diccionario (API response)."""
        # Validar campos obligatorios
        required = ['id', 'name', 'state', 'owner_id', ...]
        missing = [f for f in required if f not in data]
        if missing:
            raise ValueError(f"Faltan campos: {missing}")
        
        # Convertir tipos
        state = CourseState.from_string(data['state'])
        created_at = datetime.fromisoformat(data['created_at'])
        
        return CourseFactory.create(...)
    
    @staticmethod
    def create_for_testing(**kwargs) -> Course:
        """Crea con valores por defecto para tests."""
        return CourseFactory.create(
            id=kwargs.get('id', 'test_123'),
            name=kwargs.get('name', 'Test Course'),
            ...
        )
```

---

## ✅ POR QUÉ SÍ Factory Pattern

| Beneficio | Explicación |
|-----------|-------------|
| **Centralización** | Toda la lógica de creación en un solo lugar |
| **Validación previa** | Valida antes de crear la entidad |
| **Transformación** | Convierte tipos (string → enum, string → datetime) |
| **Normalización** | `.strip()` en strings, `None` para vacíos |
| **Testing** | `create_for_testing()` facilita escribir tests |
| **Flexibilidad** | Múltiples formas de crear (dict, parámetros, testing) |

---

## ❌ POR QUÉ NO crear directamente

```python
# ❌ ANTI-PATRÓN: Crear directamente
data = api_response  # {'id': '123', 'state': 'ACTIVE', ...}
course = Course(
    id=data['id'],
    name=data['name'],
    state=CourseState.from_string(data['state']),  # Repetitivo
    created_at=datetime.fromisoformat(data['created_at']),  # Repetitivo
    ...
)
# Problema: Esta lógica se repite en muchos lugares

# ✅ PATRÓN CORRECTO: Usar Factory
course = CourseFactory.create_from_dict(api_response)
# Beneficio: Lógica centralizada, reutilizable
```

---

## 🎓 CONCEPTOS EDUCATIVOS

### ¿Qué es el Factory Pattern?
- Patrón de diseño creacional
- Encapsula la lógica de creación de objetos
- Permite crear objetos sin especificar su clase exacta

### Tipos de Factory

```python
# 1. SIMPLE FACTORY (lo que usamos)
class CourseFactory:
    @staticmethod
    def create(...) -> Course:
        return Course(...)

# 2. FACTORY METHOD (más avanzado)
class CourseCreator(ABC):
    @abstractmethod
    def create_course(self) -> Course:
        pass

class ActiveCourseCreator(CourseCreator):
    def create_course(self) -> Course:
        return Course(state=CourseState.ACTIVE, ...)

# 3. ABSTRACT FACTORY (muy avanzado)
# Para crear familias de objetos relacionados
```

**POR QUÉ SÍ Simple Factory:**
- ✅ Suficiente para nuestras necesidades
- ✅ Fácil de entender y mantener
- ✅ No necesitamos la complejidad de Factory Method

### Normalización de Datos

```python
# Normalizar name (quitar espacios extra)
name = name.strip() if name else ""

# Normalizar section (None si está vacío)
section = section.strip() if section else None
if section == "":
    section = None

# POR QUÉ SÍ normalizar:
# ✅ Datos consistentes
# ✅ Evita "  Math  " vs "Math"
# ✅ None es mejor que "" para opcionales
```

### Validación de Campos Obligatorios

```python
required_fields = ['id', 'name', 'state', ...]
missing_fields = [f for f in required_fields if f not in data]

if missing_fields:
    raise ValueError(f"Faltan campos: {', '.join(missing_fields)}")

# POR QUÉ SÍ validar aquí:
# ✅ Fail-fast: detecta errores antes de crear
# ✅ Mensaje claro: "Faltan campos: id, name"
# ✅ Evita crear entidades inválidas
```

### Factory para Testing

```python
# ❌ SIN factory para testing
def test_course_is_active():
    course = Course(
        id="test_123",
        name="Test Course",
        state=CourseState.ACTIVE,
        owner_id="test_owner",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )  # Mucho boilerplate
    assert course.is_active()

# ✅ CON factory para testing
def test_course_is_active():
    course = CourseFactory.create_for_testing()
    assert course.is_active()
    # Más limpio, menos código
```
