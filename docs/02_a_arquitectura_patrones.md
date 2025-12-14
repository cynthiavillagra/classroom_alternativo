# 🏗️ Arquitectura y Patrones de Diseño — Classroom Explorer

> **Versión**: 1.0  
> **Fecha**: 2024-12-14  
> **Autor**: Equipo de Desarrollo  
> **Estado**: 📝 En Revisión

---

## 📑 Índice

1. [Definición de Arquitectura](#1-definición-de-arquitectura)
2. [Patrones de Diseño](#2-patrones-de-diseño)
3. [Estrategia de Integración con APIs Externas](#3-estrategia-de-integración-con-apis-externas)

---

## 1. Definición de Arquitectura

### 1.1 Arquitectura Elegida: **Clean Architecture (Arquitectura Limpia)**

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLEAN ARCHITECTURE                           │
│                   (Hexagonal/Onion)                             │
└─────────────────────────────────────────────────────────────────┘

        ┌───────────────────────────────────────────┐
        │         🎨 PRESENTATION LAYER             │
        │      (Frontend: HTML/CSS/JS)              │
        │   • UI Components                         │
        │   • Event Handlers                        │
        │   • HTTP Client                           │
        └──────────────────┬────────────────────────┘
                           │
                           │ HTTP/REST
                           │
        ┌──────────────────▼────────────────────────┐
        │         🔌 API LAYER                      │
        │      (Vercel Serverless)                  │
        │   • Routes/Endpoints                      │
        │   • Request Validation                    │
        │   • Response Serialization                │
        └──────────────────┬────────────────────────┘
                           │
                           │ Dependency Injection
                           │
        ┌──────────────────▼────────────────────────┐
        │      ⚙️ APPLICATION LAYER                 │
        │         (Use Cases)                       │
        │   • Business Logic Orchestration          │
        │   • No conoce detalles de DB/API          │
        └──────────────────┬────────────────────────┘
                           │
                           │ Interfaces (Ports)
                           │
        ┌──────────────────▼────────────────────────┐
        │       🏛️ DOMAIN LAYER                     │
        │      (Entities + Rules)                   │
        │   • Course, Material (POO pura)           │
        │   • Business Rules                        │
        │   • NO dependencias externas              │
        └──────────────────┬────────────────────────┘
                           │
                           │ Interfaces (Ports)
                           │
        ┌──────────────────▼────────────────────────┐
        │     🔧 INFRASTRUCTURE LAYER                │
        │      (Adapters/Implementations)           │
        │   • GoogleClassroomClient                 │
        │   • GoogleOAuthClient                     │
        │   • Mappers (API → Domain)                │
        └───────────────────────────────────────────┘
                           │
                           │ HTTP
                           │
        ┌──────────────────▼────────────────────────┐
        │      🌐 EXTERNAL SERVICES                 │
        │   • Google Classroom API                  │
        │   • Google OAuth 2.0                      │
        └───────────────────────────────────────────┘
```

---

### 1.2 Justificación: ¿Por Qué SÍ Clean Architecture?

#### ✅ **Razones Técnicas**

| Beneficio | Explicación | Impacto en Nuestro Proyecto |
|-----------|-------------|----------------------------|
| **Independencia de Frameworks** | El dominio no depende de librerías externas | Si Google cambia su API, solo tocamos Infrastructure |
| **Testeable** | Cada capa se puede testear aisladamente | Tests unitarios del dominio sin llamadas HTTP reales |
| **Mantenible** | Separación clara de responsabilidades | Código fácil de entender para aprendizaje |
| **Escalable** | Agregar features no rompe lo existente | Podemos agregar Supabase después sin refactorizar |
| **Educativo** | Patrón profesional de la industria | Aprendes arquitectura real, no código "de tutorial" |

#### ✅ **Por Qué SÍ es Ideal para Nuestro Stack**

```
CONTEXTO: Python + Vercel Serverless + Google API

┌─────────────────────────────────────────────────────────────────┐
│  VENTAJA 1: Serverless-Friendly                                 │
│  ────────────────────────────────────────────────────────────   │
│  • Cada función Vercel es stateless                             │
│  • Clean Architecture facilita funciones puras                  │
│  • Dependency Injection manual (sin frameworks pesados)         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  VENTAJA 2: Aislamiento de APIs Externas                        │
│  ────────────────────────────────────────────────────────────   │
│  • Google API está en Infrastructure (adaptador)                │
│  • Si Google depreca un endpoint, solo cambiamos el adapter     │
│  • El dominio (Course, Material) nunca cambia                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  VENTAJA 3: Testing Sin Dependencias                            │
│  ────────────────────────────────────────────────────────────   │
│  • Podemos testear Use Cases con mocks                          │
│  • No necesitamos credenciales de Google para tests             │
│  • CI/CD más rápido y confiable                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  VENTAJA 4: Aprendizaje Progresivo                              │
│  ────────────────────────────────────────────────────────────   │
│  • Empezamos con Domain (POO pura, sin complejidad)             │
│  • Luego Infrastructure (HTTP, APIs)                            │
│  • Finalmente integramos todo                                   │
│  • Cada capa es un "mini-proyecto" comprensible                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 1.3 Comparación: ¿Por Qué NO Otras Arquitecturas?

#### ❌ **Arquitectura Monolítica (Todo en un archivo)**

```python
# ❌ ANTI-PATRÓN: Todo mezclado
def get_courses():
    # Lógica de negocio + HTTP + Validación + Mapeo
    token = request.headers['Authorization']
    response = requests.get('https://classroom.googleapis.com/v1/courses',
                           headers={'Authorization': token})
    courses = []
    for item in response.json()['courses']:
        courses.append({
            'id': item['id'],
            'name': item['name']
        })
    return jsonify(courses)
```

**Problemas:**
- 🔴 Imposible testear sin hacer llamadas HTTP reales
- 🔴 Si Google cambia la respuesta, hay que buscar en todo el código
- 🔴 No se puede reutilizar la lógica en otros endpoints
- 🔴 Código difícil de entender y mantener

---

#### ❌ **MVC Tradicional (Model-View-Controller)**

```
POR QUÉ NO:
• MVC está diseñado para apps con UI server-side (Django, Rails)
• Nosotros tenemos frontend separado (SPA)
• MVC no separa bien lógica de negocio de infraestructura
• El "Model" suele estar acoplado a la base de datos
```

**Cuándo SÍ usar MVC:**
- Apps con templates server-side (Jinja, EJS)
- Proyectos pequeños sin APIs externas complejas

---

#### ❌ **Microservicios**

```
POR QUÉ NO (para este proyecto):
• Overkill para un MVP educativo
• Complejidad de orquestación innecesaria
• Más difícil de debuggear localmente
• Requiere infraestructura compleja (Docker, K8s)
```

**Cuándo SÍ usar Microservicios:**
- Equipos grandes (> 5 personas)
- Necesidad de escalar servicios independientemente
- Dominios de negocio muy separados

---

### 1.4 Reglas de Dependencia (The Dependency Rule)

```
┌─────────────────────────────────────────────────────────────────┐
│                   REGLA DE ORO                                  │
│  ─────────────────────────────────────────────────────────────  │
│  Las dependencias SIEMPRE apuntan hacia adentro (hacia Domain)  │
│                                                                 │
│  ✅ Infrastructure puede importar Domain                        │
│  ✅ Application puede importar Domain                           │
│  ❌ Domain NO puede importar Infrastructure                     │
│  ❌ Domain NO puede importar Application                        │
└─────────────────────────────────────────────────────────────────┘
```

#### Ejemplo Práctico:

```python
# ✅ CORRECTO: Infrastructure importa Domain
# api/infrastructure/google_classroom_client.py
from api.domain.entities.course import Course  # ✅ OK

class GoogleClassroomClient:
    def get_courses(self) -> list[Course]:
        # Llama a Google API y convierte a Course
        pass
```

```python
# ❌ INCORRECTO: Domain importa Infrastructure
# api/domain/entities/course.py
from api.infrastructure.google_classroom_client import GoogleClassroomClient  # ❌ MAL

class Course:
    def __init__(self, id: str, name: str):
        self.client = GoogleClassroomClient()  # ❌ Acoplamiento!
```

**Por qué es importante:**
- El dominio debe ser **puro** (sin dependencias externas)
- Podemos cambiar Google API por otra fuente sin tocar el dominio
- Los tests del dominio no necesitan mocks de HTTP

---

## 2. Patrones de Diseño

### 2.1 Diccionario de Patrones Aplicados

| Patrón | Categoría | Dónde lo Usamos | Problema que Resuelve |
|--------|-----------|-----------------|----------------------|
| **Repository** | Creacional | Infrastructure | Abstrae el acceso a datos (Google API) |
| **Adapter** | Estructural | Infrastructure | Convierte respuestas de Google API a entidades de dominio |
| **Dependency Injection** | Creacional | Application/API | Desacopla componentes, facilita testing |
| **Factory** | Creacional | Domain | Crea entidades con validaciones |
| **Strategy** | Comportamiento | Application | Diferentes estrategias de filtrado |
| **Singleton** | Creacional | Infrastructure | Cliente HTTP reutilizable |

---

### 2.2 Patrón 1: **Repository Pattern**

#### 📖 Definición

> Abstrae la lógica de acceso a datos, permitiendo que la aplicación trabaje con una interfaz sin conocer el origen real de los datos.

#### 🎯 Problema que Resuelve

```
PROBLEMA:
• Los Use Cases necesitan obtener cursos y materiales
• Pero NO deben saber si vienen de Google API, Supabase o un archivo JSON
• Si cambiamos la fuente de datos, no queremos reescribir toda la app
```

#### ✅ Solución con Repository

```python
# ═══════════════════════════════════════════════════════════════
# PASO 1: Definir la interfaz (Port) en Domain
# api/domain/interfaces/classroom_repository.py
# ═══════════════════════════════════════════════════════════════
from abc import ABC, abstractmethod
from typing import List
from api.domain.entities.course import Course
from api.domain.entities.material import Material

class ClassroomRepository(ABC):
    """
    Interfaz que define CÓMO obtener datos de Classroom.
    NO define DE DÓNDE vienen (eso es responsabilidad de Infrastructure).
    """
    
    @abstractmethod
    def get_user_courses(self, user_id: str) -> List[Course]:
        """Obtiene todos los cursos del usuario."""
        pass
    
    @abstractmethod
    def get_course_materials(self, course_id: str) -> List[Material]:
        """Obtiene todos los materiales de un curso."""
        pass
```

```python
# ═══════════════════════════════════════════════════════════════
# PASO 2: Implementar el adaptador en Infrastructure
# api/infrastructure/repositories/google_classroom_repository.py
# ═══════════════════════════════════════════════════════════════
from api.domain.interfaces.classroom_repository import ClassroomRepository
from api.infrastructure.google_classroom_client import GoogleClassroomClient
from api.infrastructure.mappers.classroom_mapper import ClassroomMapper

class GoogleClassroomRepository(ClassroomRepository):
    """
    Implementación concreta que obtiene datos de Google Classroom API.
    """
    
    def __init__(self, client: GoogleClassroomClient):
        self.client = client
        self.mapper = ClassroomMapper()
    
    def get_user_courses(self, user_id: str) -> List[Course]:
        # 1. Llamar a Google API
        api_response = self.client.list_courses(user_id)
        
        # 2. Convertir respuesta a entidades de dominio
        courses = [
            self.mapper.api_course_to_domain(course_data)
            for course_data in api_response.get('courses', [])
        ]
        
        return courses
    
    def get_course_materials(self, course_id: str) -> List[Material]:
        # Similar al anterior
        api_response = self.client.list_course_work(course_id)
        materials = [
            self.mapper.api_material_to_domain(material_data)
            for material_data in api_response.get('courseWork', [])
        ]
        return materials
```

```python
# ═══════════════════════════════════════════════════════════════
# PASO 3: Usar en Application (Use Case)
# api/application/use_cases/list_courses.py
# ═══════════════════════════════════════════════════════════════
from api.domain.interfaces.classroom_repository import ClassroomRepository

class ListUserCoursesUseCase:
    """
    Caso de uso: Listar cursos del usuario.
    NO sabe si los datos vienen de Google, Supabase o un mock.
    """
    
    def __init__(self, repository: ClassroomRepository):
        # Recibe la INTERFAZ, no la implementación concreta
        self.repository = repository
    
    def execute(self, user_id: str):
        # Simplemente usa el repository
        courses = self.repository.get_user_courses(user_id)
        return courses
```

#### 🎓 Por Qué SÍ

- ✅ **Testeable**: Podemos crear un `MockClassroomRepository` para tests
- ✅ **Flexible**: Mañana podemos agregar `SupabaseClassroomRepository` sin tocar Use Cases
- ✅ **Desacoplado**: Application no conoce detalles de HTTP, tokens, etc.

#### ⚠️ Por Qué NO (Anti-patrón)

```python
# ❌ MAL: Use Case acoplado a Google API
class ListUserCoursesUseCase:
    def execute(self, user_id: str, access_token: str):
        # ❌ Conoce detalles de implementación
        response = requests.get(
            'https://classroom.googleapis.com/v1/courses',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        # ❌ Imposible testear sin llamadas HTTP reales
        # ❌ Si cambiamos a otra API, hay que reescribir esto
        return response.json()['courses']
```

---

### 2.3 Patrón 2: **Adapter Pattern**

#### 📖 Definición

> Convierte la interfaz de una clase en otra interfaz que el cliente espera. Permite que clases incompatibles trabajen juntas.

#### 🎯 Problema que Resuelve

```
PROBLEMA:
• Google Classroom API devuelve JSON con estructura específica
• Nuestro dominio usa objetos Python (Course, Material)
• No queremos que el dominio dependa del formato de Google
```

#### ✅ Solución con Adapter (Mapper)

```python
# ═══════════════════════════════════════════════════════════════
# Respuesta de Google API (lo que recibimos)
# ═══════════════════════════════════════════════════════════════
{
    "id": "123456",
    "name": "Matemáticas 3°A",
    "section": "Turno Mañana",
    "courseState": "ACTIVE",
    "creationTime": "2024-01-15T10:00:00.000Z"
}
```

```python
# ═══════════════════════════════════════════════════════════════
# api/infrastructure/mappers/classroom_mapper.py
# ═══════════════════════════════════════════════════════════════
from datetime import datetime
from api.domain.entities.course import Course
from api.domain.entities.material import Material, MaterialType

class ClassroomMapper:
    """
    Adapter que convierte respuestas de Google API a entidades de dominio.
    """
    
    def api_course_to_domain(self, api_data: dict) -> Course:
        """
        Convierte un curso de Google API a nuestra entidad Course.
        
        POR QUÉ SÍ:
        • Si Google cambia el formato, solo tocamos este método
        • El dominio nunca ve el JSON de Google
        """
        return Course(
            id=api_data['id'],
            name=api_data['name'],
            section=api_data.get('section'),  # Puede ser None
            state=api_data.get('courseState', 'UNKNOWN'),
            created_at=self._parse_google_timestamp(api_data.get('creationTime'))
        )
    
    def api_material_to_domain(self, api_data: dict) -> Material:
        """Convierte un material de Google API a nuestra entidad Material."""
        
        # Determinar el tipo de material
        material_type = self._detect_material_type(api_data)
        
        # Extraer la URL según el tipo
        url = self._extract_material_url(api_data, material_type)
        
        return Material(
            id=api_data['id'],
            title=api_data.get('title', 'Sin título'),
            type=material_type,
            url=url,
            course_id=api_data['courseId'],
            created_at=self._parse_google_timestamp(api_data.get('creationTime'))
        )
    
    def _detect_material_type(self, api_data: dict) -> MaterialType:
        """
        Detecta el tipo de material según la estructura de Google API.
        
        POR QUÉ SÍ este método privado:
        • Encapsula lógica compleja de detección
        • Reutilizable en otros mappers
        """
        if 'materials' in api_data:
            materials = api_data['materials']
            if any('driveFile' in m for m in materials):
                # Detectar por extensión
                drive_file = next(m['driveFile'] for m in materials if 'driveFile' in m)
                title = drive_file.get('title', '')
                
                if title.endswith('.pdf'):
                    return MaterialType.PDF
                elif title.endswith(('.doc', '.docx')):
                    return MaterialType.DOCUMENT
                elif title.endswith(('.jpg', '.png', '.gif')):
                    return MaterialType.IMAGE
                else:
                    return MaterialType.FILE
            
            elif any('youtubeVideo' in m for m in materials):
                return MaterialType.VIDEO
            
            elif any('link' in m for m in materials):
                return MaterialType.LINK
            
            elif any('form' in m for m in materials):
                return MaterialType.FORM
        
        return MaterialType.ASSIGNMENT  # Por defecto
    
    def _extract_material_url(self, api_data: dict, material_type: MaterialType) -> str:
        """Extrae la URL del material según su tipo."""
        materials = api_data.get('materials', [])
        
        if not materials:
            return f"https://classroom.google.com/c/{api_data['courseId']}/a/{api_data['id']}"
        
        material = materials[0]
        
        if 'driveFile' in material:
            return material['driveFile'].get('alternateLink', '')
        elif 'youtubeVideo' in material:
            return material['youtubeVideo'].get('alternateLink', '')
        elif 'link' in material:
            return material['link'].get('url', '')
        elif 'form' in material:
            return material['form'].get('formUrl', '')
        
        return ''
    
    def _parse_google_timestamp(self, timestamp_str: str) -> datetime:
        """Convierte timestamp de Google a datetime de Python."""
        if not timestamp_str:
            return datetime.now()
        
        # Google usa ISO 8601
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
```

#### 🎓 Por Qué SÍ

- ✅ **Aislamiento**: El dominio nunca ve el JSON de Google
- ✅ **Mantenible**: Si Google cambia el formato, solo tocamos el mapper
- ✅ **Testeable**: Podemos testear el mapper con JSONs de ejemplo

#### ⚠️ Por Qué NO (Anti-patrón)

```python
# ❌ MAL: Entidad de dominio conoce el formato de Google
class Course:
    def __init__(self, google_api_response: dict):
        # ❌ Acoplamiento directo a Google
        self.id = google_api_response['id']
        self.name = google_api_response['name']
        # ❌ Si Google cambia, hay que modificar la entidad
```

---

### 2.4 Patrón 3: **Dependency Injection (DI)**

#### 📖 Definición

> En lugar de que una clase cree sus dependencias, se las pasamos desde afuera (inyección).

#### 🎯 Problema que Resuelve

```
PROBLEMA:
• Los Use Cases necesitan un Repository
• Si el Use Case crea el Repository internamente, queda acoplado
• No podemos testear con mocks
```

#### ✅ Solución con Dependency Injection

```python
# ═══════════════════════════════════════════════════════════════
# ❌ SIN Dependency Injection (Acoplado)
# ═══════════════════════════════════════════════════════════════
class ListUserCoursesUseCase:
    def __init__(self):
        # ❌ Crea su propia dependencia
        self.repository = GoogleClassroomRepository()
    
    def execute(self, user_id: str):
        return self.repository.get_user_courses(user_id)

# PROBLEMA: No puedo testear con un mock, siempre usa Google API
```

```python
# ═══════════════════════════════════════════════════════════════
# ✅ CON Dependency Injection (Desacoplado)
# ═══════════════════════════════════════════════════════════════
class ListUserCoursesUseCase:
    def __init__(self, repository: ClassroomRepository):
        # ✅ Recibe la dependencia desde afuera
        self.repository = repository
    
    def execute(self, user_id: str):
        return self.repository.get_user_courses(user_id)

# VENTAJA: Puedo inyectar un mock en tests
```

```python
# ═══════════════════════════════════════════════════════════════
# Uso en producción (api/routes/courses.py)
# ═══════════════════════════════════════════════════════════════
from api.infrastructure.repositories.google_classroom_repository import GoogleClassroomRepository
from api.infrastructure.google_classroom_client import GoogleClassroomClient
from api.application.use_cases.list_courses import ListUserCoursesUseCase

def get_courses_endpoint(user_id: str):
    # Crear dependencias
    client = GoogleClassroomClient()
    repository = GoogleClassroomRepository(client)
    
    # Inyectar en Use Case
    use_case = ListUserCoursesUseCase(repository)
    
    # Ejecutar
    courses = use_case.execute(user_id)
    return courses
```

```python
# ═══════════════════════════════════════════════════════════════
# Uso en tests (tests/unit/test_list_courses.py)
# ═══════════════════════════════════════════════════════════════
class MockClassroomRepository(ClassroomRepository):
    def get_user_courses(self, user_id: str):
        # Devuelve datos fake
        return [
            Course(id='1', name='Matemáticas', section='3A', state='ACTIVE'),
            Course(id='2', name='Historia', section='3A', state='ACTIVE')
        ]

def test_list_courses():
    # Inyectar mock
    mock_repo = MockClassroomRepository()
    use_case = ListUserCoursesUseCase(mock_repo)
    
    # Ejecutar sin llamadas HTTP reales
    courses = use_case.execute('user123')
    
    assert len(courses) == 2
    assert courses[0].name == 'Matemáticas'
```

#### 🎓 Por Qué SÍ

- ✅ **Testeable**: Podemos inyectar mocks
- ✅ **Flexible**: Podemos cambiar implementaciones sin tocar el Use Case
- ✅ **Explícito**: Las dependencias son visibles en el constructor

---

### 2.5 Patrón 4: **Factory Pattern**

#### 📖 Definición

> Encapsula la lógica de creación de objetos complejos.

#### 🎯 Problema que Resuelve

```
PROBLEMA:
• Crear un Material requiere validaciones y lógica compleja
• No queremos duplicar esa lógica en múltiples lugares
```

#### ✅ Solución con Factory

```python
# ═══════════════════════════════════════════════════════════════
# api/domain/entities/material.py
# ═══════════════════════════════════════════════════════════════
from enum import Enum
from datetime import datetime
from dataclasses import dataclass

class MaterialType(Enum):
    PDF = 'pdf'
    VIDEO = 'video'
    DOCUMENT = 'document'
    LINK = 'link'
    FORM = 'form'
    IMAGE = 'image'
    ASSIGNMENT = 'assignment'
    FILE = 'file'

@dataclass
class Material:
    id: str
    title: str
    type: MaterialType
    url: str
    course_id: str
    created_at: datetime
    
    def __post_init__(self):
        """Validaciones automáticas al crear."""
        if not self.id:
            raise ValueError("Material ID no puede estar vacío")
        if not self.title:
            raise ValueError("Material title no puede estar vacío")
        if not isinstance(self.type, MaterialType):
            raise ValueError(f"Tipo inválido: {self.type}")
```

```python
# ═══════════════════════════════════════════════════════════════
# api/domain/factories/material_factory.py
# ═══════════════════════════════════════════════════════════════
from api.domain.entities.material import Material, MaterialType
from datetime import datetime

class MaterialFactory:
    """
    Factory para crear Materials con validaciones y defaults.
    
    POR QUÉ SÍ:
    • Centraliza la lógica de creación
    • Aplica validaciones consistentes
    • Facilita crear Materials en tests
    """
    
    @staticmethod
    def create(
        id: str,
        title: str,
        type: MaterialType,
        url: str,
        course_id: str,
        created_at: datetime = None
    ) -> Material:
        """Crea un Material con validaciones."""
        
        # Aplicar defaults
        if created_at is None:
            created_at = datetime.now()
        
        # Validaciones adicionales
        if not url.startswith('http'):
            raise ValueError(f"URL inválida: {url}")
        
        # Crear entidad
        return Material(
            id=id,
            title=title.strip(),  # Limpiar espacios
            type=type,
            url=url,
            course_id=course_id,
            created_at=created_at
        )
    
    @staticmethod
    def create_from_dict(data: dict) -> Material:
        """Crea un Material desde un diccionario."""
        return MaterialFactory.create(
            id=data['id'],
            title=data['title'],
            type=MaterialType(data['type']),
            url=data['url'],
            course_id=data['course_id'],
            created_at=data.get('created_at')
        )
```

#### 🎓 Por Qué SÍ

- ✅ **Consistencia**: Todas las validaciones en un solo lugar
- ✅ **Testeable**: Fácil crear Materials en tests
- ✅ **Mantenible**: Si cambian las reglas, solo tocamos el Factory

---

### 2.6 Patrón 5: **Strategy Pattern**

#### 📖 Definición

> Define una familia de algoritmos, encapsula cada uno y los hace intercambiables.

#### 🎯 Problema que Resuelve

```
PROBLEMA:
• Necesitamos filtrar materiales por diferentes criterios
• No queremos un if/else gigante
• Queremos poder agregar nuevos filtros fácilmente
```

#### ✅ Solución con Strategy

```python
# ═══════════════════════════════════════════════════════════════
# api/application/filters/material_filter_strategy.py
# ═══════════════════════════════════════════════════════════════
from abc import ABC, abstractmethod
from typing import List
from api.domain.entities.material import Material, MaterialType
from datetime import datetime

class MaterialFilterStrategy(ABC):
    """Interfaz para estrategias de filtrado."""
    
    @abstractmethod
    def filter(self, materials: List[Material]) -> List[Material]:
        pass

class FilterByType(MaterialFilterStrategy):
    """Filtra materiales por tipo."""
    
    def __init__(self, material_type: MaterialType):
        self.material_type = material_type
    
    def filter(self, materials: List[Material]) -> List[Material]:
        return [m for m in materials if m.type == self.material_type]

class FilterByDateRange(MaterialFilterStrategy):
    """Filtra materiales por rango de fechas."""
    
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date
    
    def filter(self, materials: List[Material]) -> List[Material]:
        return [
            m for m in materials
            if self.start_date <= m.created_at <= self.end_date
        ]

class FilterByCourse(MaterialFilterStrategy):
    """Filtra materiales por curso."""
    
    def __init__(self, course_id: str):
        self.course_id = course_id
    
    def filter(self, materials: List[Material]) -> List[Material]:
        return [m for m in materials if m.course_id == self.course_id]
```

```python
# ═══════════════════════════════════════════════════════════════
# api/application/use_cases/filter_materials.py
# ═══════════════════════════════════════════════════════════════
from typing import List
from api.domain.entities.material import Material
from api.application.filters.material_filter_strategy import MaterialFilterStrategy

class FilterMaterialsUseCase:
    """
    Aplica múltiples filtros a una lista de materiales.
    
    POR QUÉ SÍ Strategy:
    • Podemos combinar filtros fácilmente
    • Agregar nuevos filtros no requiere modificar este código
    """
    
    def execute(
        self,
        materials: List[Material],
        filters: List[MaterialFilterStrategy]
    ) -> List[Material]:
        """
        Aplica todos los filtros en secuencia.
        
        Args:
            materials: Lista inicial de materiales
            filters: Lista de estrategias de filtrado
        
        Returns:
            Materiales que pasan todos los filtros
        """
        result = materials
        
        for filter_strategy in filters:
            result = filter_strategy.filter(result)
        
        return result
```

```python
# ═══════════════════════════════════════════════════════════════
# Uso en API (api/routes/materials.py)
# ═══════════════════════════════════════════════════════════════
from api.application.filters.material_filter_strategy import (
    FilterByType, FilterByDateRange, FilterByCourse
)

def filter_materials_endpoint(materials, query_params):
    filters = []
    
    # Construir filtros según query params
    if 'type' in query_params:
        filters.append(FilterByType(MaterialType(query_params['type'])))
    
    if 'course_id' in query_params:
        filters.append(FilterByCourse(query_params['course_id']))
    
    if 'start_date' in query_params and 'end_date' in query_params:
        filters.append(FilterByDateRange(
            start_date=parse_date(query_params['start_date']),
            end_date=parse_date(query_params['end_date'])
        ))
    
    # Aplicar filtros
    use_case = FilterMaterialsUseCase()
    filtered = use_case.execute(materials, filters)
    
    return filtered
```

#### 🎓 Por Qué SÍ

- ✅ **Extensible**: Agregar filtros no modifica código existente
- ✅ **Combinable**: Podemos aplicar múltiples filtros
- ✅ **Testeable**: Cada filtro se testea aisladamente

---

### 2.7 Patrón 6: **Singleton Pattern**

#### 📖 Definición

> Garantiza que una clase tenga una única instancia y proporciona un punto de acceso global.

#### 🎯 Problema que Resuelve

```
PROBLEMA:
• El cliente HTTP para Google API es costoso de crear
• No queremos crear una instancia nueva en cada request
• Necesitamos reutilizar la conexión
```

#### ✅ Solución con Singleton

```python
# ═══════════════════════════════════════════════════════════════
# api/infrastructure/google_classroom_client.py
# ═══════════════════════════════════════════════════════════════
import requests
from typing import Optional

class GoogleClassroomClient:
    """
    Cliente HTTP para Google Classroom API (Singleton).
    
    POR QUÉ SÍ Singleton:
    • Reutiliza la sesión HTTP (connection pooling)
    • Evita crear múltiples instancias en Vercel
    """
    
    _instance: Optional['GoogleClassroomClient'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa la sesión HTTP una sola vez."""
        self.session = requests.Session()
        self.base_url = 'https://classroom.googleapis.com/v1'
    
    def list_courses(self, access_token: str) -> dict:
        """Lista cursos del usuario."""
        response = self.session.get(
            f'{self.base_url}/courses',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        response.raise_for_status()
        return response.json()
    
    def list_course_work(self, course_id: str, access_token: str) -> dict:
        """Lista materiales de un curso."""
        response = self.session.get(
            f'{self.base_url}/courses/{course_id}/courseWork',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        response.raise_for_status()
        return response.json()
```

#### 🎓 Por Qué SÍ

- ✅ **Eficiente**: Reutiliza conexiones HTTP
- ✅ **Simple**: No necesitamos gestionar instancias manualmente

#### ⚠️ Cuándo NO usar Singleton

```
❌ NO usar para:
• Clases con estado mutable compartido (race conditions)
• Cuando necesitas múltiples configuraciones
• En tests (dificulta el aislamiento)

✅ Alternativa en tests:
• Inyectar un mock en lugar del Singleton
```

---

## 3. Estrategia de Integración con APIs Externas

### 3.1 Arquitectura de Integración

```
┌─────────────────────────────────────────────────────────────────┐
│                    NUESTRA APLICACIÓN                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Application Layer (Use Cases)                            │  │
│  │  • No conoce detalles de Google API                       │  │
│  │  • Trabaja con interfaces (Ports)                         │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │                                        │
│                        │ Usa interfaz                           │
│                        │                                        │
│  ┌─────────────────────▼─────────────────────────────────────┐  │
│  │  Domain Interfaces (Ports)                                │  │
│  │  • ClassroomRepository (interfaz)                         │  │
│  │  • Define QUÉ necesitamos, no CÓMO obtenerlo              │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │                                        │
│                        │ Implementado por                       │
│                        │                                        │
│  ┌─────────────────────▼─────────────────────────────────────┐  │
│  │  Infrastructure - Adapters                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │  GoogleClassroomRepository (Adapter)                │  │  │
│  │  │  • Implementa la interfaz                           │  │  │
│  │  │  • Usa GoogleClassroomClient                        │  │  │
│  │  │  • Usa ClassroomMapper                              │  │  │
│  │  └──────────────────┬──────────────────────────────────┘  │  │
│  │                     │                                     │  │
│  │  ┌──────────────────▼──────────────────────────────────┐  │  │
│  │  │  GoogleClassroomClient (HTTP Client)                │  │  │
│  │  │  • Maneja requests HTTP                             │  │  │
│  │  │  • Maneja autenticación                             │  │  │
│  │  │  • Maneja errores y reintentos                      │  │  │
│  │  └──────────────────┬──────────────────────────────────┘  │  │
│  │                     │                                     │  │
│  │  ┌──────────────────▼──────────────────────────────────┐  │  │
│  │  │  ClassroomMapper (Adapter)                          │  │  │
│  │  │  • Convierte JSON de Google → Entidades Domain      │  │  │
│  │  │  • Aísla cambios en formato de API                  │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                        │                                        │
└────────────────────────┼────────────────────────────────────────┘
                         │ HTTP/REST
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              GOOGLE CLASSROOM API (Externa)                     │
│  • Fuera de nuestro control                                     │
│  • Puede cambiar sin previo aviso                               │
│  • Tiene rate limits y errores                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 3.2 Patrón: **Hexagonal Architecture (Ports & Adapters)**

#### 📖 Concepto

```
PORTS (Puertos):
• Interfaces que definen CÓMO nuestra app se comunica con el exterior
• Viven en Domain/Application
• Ejemplo: ClassroomRepository

ADAPTERS (Adaptadores):
• Implementaciones concretas de los Ports
• Viven en Infrastructure
• Ejemplo: GoogleClassroomRepository
```

#### ✅ Beneficios

| Beneficio | Explicación |
|-----------|-------------|
| **Aislamiento** | Si Google cambia su API, solo tocamos el Adapter |
| **Testeable** | Podemos crear MockAdapters para tests |
| **Intercambiable** | Podemos cambiar Google por otra fuente sin tocar el core |
| **Resiliente** | Errores de API no rompen la lógica de negocio |

---

### 3.3 Manejo de Cambios en APIs Externas

#### Escenario 1: Google Cambia el Formato de Respuesta

```python
# ═══════════════════════════════════════════════════════════════
# ANTES: Google devolvía
# ═══════════════════════════════════════════════════════════════
{
    "id": "123",
    "name": "Matemáticas"
}

# ═══════════════════════════════════════════════════════════════
# DESPUÉS: Google cambia a
# ═══════════════════════════════════════════════════════════════
{
    "courseId": "123",
    "courseName": "Matemáticas"
}

# ═══════════════════════════════════════════════════════════════
# SOLUCIÓN: Solo modificamos el Mapper
# ═══════════════════════════════════════════════════════════════
class ClassroomMapper:
    def api_course_to_domain(self, api_data: dict) -> Course:
        # Soportar ambos formatos (backward compatibility)
        course_id = api_data.get('courseId') or api_data.get('id')
        course_name = api_data.get('courseName') or api_data.get('name')
        
        return Course(id=course_id, name=course_name)

# ✅ El resto de la app NO se entera del cambio
```

#### Escenario 2: Google Depreca un Endpoint

```python
# ═══════════════════════════════════════════════════════════════
# ANTES: Usábamos /v1/courses
# DESPUÉS: Google depreca y obliga a usar /v2/courses
# ═══════════════════════════════════════════════════════════════

# SOLUCIÓN: Solo modificamos el Client
class GoogleClassroomClient:
    def __init__(self):
        # Cambiar versión de API
        self.base_url = 'https://classroom.googleapis.com/v2'  # ✅ Un solo cambio
    
    # El resto del código sigue igual

# ✅ Use Cases y Domain no se enteran
```

---

### 3.4 Manejo de Errores de API

```python
# ═══════════════════════════════════════════════════════════════
# api/infrastructure/google_classroom_client.py
# ═══════════════════════════════════════════════════════════════
import time
from requests.exceptions import RequestException

class GoogleClassroomClient:
    """
    Cliente con manejo robusto de errores.
    
    POR QUÉ SÍ:
    • Las APIs externas fallan (network, rate limits, etc.)
    • Necesitamos reintentos automáticos
    • Necesitamos mensajes de error claros
    """
    
    def _make_request(
        self,
        method: str,
        url: str,
        headers: dict,
        max_retries: int = 3
    ) -> dict:
        """
        Hace un request con reintentos y backoff exponencial.
        """
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, headers=headers)
                
                # Manejar rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 2 ** attempt))
                    time.sleep(retry_after)
                    continue
                
                # Manejar errores HTTP
                response.raise_for_status()
                
                return response.json()
            
            except RequestException as e:
                if attempt == max_retries - 1:
                    # Último intento, propagar error
                    raise GoogleAPIError(f"Error al conectar con Google API: {e}")
                
                # Backoff exponencial: 1s, 2s, 4s
                time.sleep(2 ** attempt)
        
        raise GoogleAPIError("Max retries alcanzado")

class GoogleAPIError(Exception):
    """Excepción personalizada para errores de Google API."""
    pass
```

---

### 3.5 Gestión de Variables de Entorno (Seguridad)

#### 🔐 Regla de Oro: **NUNCA hardcodear credenciales**

```python
# ═══════════════════════════════════════════════════════════════
# ❌ MAL: Credenciales hardcodeadas
# ═══════════════════════════════════════════════════════════════
GOOGLE_CLIENT_ID = "123456-abcdef.apps.googleusercontent.com"  # ❌ NUNCA
GOOGLE_CLIENT_SECRET = "GOCSPX-abc123def456"  # ❌ PELIGRO
```

```python
# ═══════════════════════════════════════════════════════════════
# ✅ BIEN: Variables de entorno
# api/infrastructure/config.py
# ═══════════════════════════════════════════════════════════════
import os
from typing import Optional

class Config:
    """
    Configuración centralizada de la aplicación.
    
    POR QUÉ SÍ:
    • Todas las variables de entorno en un solo lugar
    • Validación al inicio de la app
    • Fácil de testear con valores mock
    """
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET', '')
    OAUTH_REDIRECT_URI: str = os.getenv('OAUTH_REDIRECT_URI', 'http://localhost:3000/api/auth/callback')
    
    # App
    APP_URL: str = os.getenv('APP_URL', 'http://localhost:3000')
    SESSION_SECRET: str = os.getenv('SESSION_SECRET', '')
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    
    @classmethod
    def validate(cls):
        """
        Valida que todas las variables críticas estén configuradas.
        Llamar al inicio de la app.
        """
        errors = []
        
        if not cls.GOOGLE_CLIENT_ID:
            errors.append("GOOGLE_CLIENT_ID no está configurado")
        
        if not cls.GOOGLE_CLIENT_SECRET:
            errors.append("GOOGLE_CLIENT_SECRET no está configurado")
        
        if not cls.SESSION_SECRET and cls.ENVIRONMENT == 'production':
            errors.append("SESSION_SECRET es obligatorio en producción")
        
        if errors:
            raise ValueError(f"Errores de configuración:\n" + "\n".join(errors))
    
    @classmethod
    def is_production(cls) -> bool:
        return cls.ENVIRONMENT == 'production'
```

```python
# ═══════════════════════════════════════════════════════════════
# Uso en la aplicación
# ═══════════════════════════════════════════════════════════════
from api.infrastructure.config import Config

# Al inicio de la app (en main o __init__)
Config.validate()  # ✅ Falla rápido si falta algo

# En cualquier parte del código
client_id = Config.GOOGLE_CLIENT_ID  # ✅ Seguro
```

---

### 3.6 Checklist de Seguridad para APIs Externas

| ✅ | Práctica | Implementación |
|----|----------|----------------|
| ✅ | Variables de entorno | `.env` + `Config` class |
| ✅ | Tokens nunca en código | `os.getenv()` siempre |
| ✅ | Tokens nunca en logs | Sanitizar logs antes de escribir |
| ✅ | HTTPS obligatorio | Validar URLs en Config |
| ✅ | Timeout en requests | `requests.get(timeout=10)` |
| ✅ | Rate limiting | Backoff exponencial |
| ✅ | Validación de respuestas | Schemas con validación |
| ✅ | Manejo de errores | Try/except con mensajes claros |

---

## 📎 Resumen Ejecutivo

### Decisiones Arquitectónicas Clave

| Decisión | Justificación |
|----------|---------------|
| **Clean Architecture** | Separación de capas, testeable, mantenible |
| **Repository Pattern** | Abstrae acceso a datos (Google API) |
| **Adapter Pattern** | Aísla cambios en formato de API externa |
| **Dependency Injection** | Desacopla componentes, facilita testing |
| **Strategy Pattern** | Filtros extensibles y combinables |
| **Hexagonal Architecture** | Ports & Adapters para APIs externas |

### Próximo Paso

Una vez aprobado este documento, pasaremos a:
- **Parte B**: Diagramas UML (Clases, Secuencia, Componentes)
- **Parte C**: Modelo de datos y mapa de endpoints

---

## ✅ Checklist de Aprobación

- [ ] Arquitectura Clean Architecture entendida
- [ ] Patrones de diseño justificados
- [ ] Estrategia de integración con Google API clara
- [ ] Gestión de variables de entorno aprobada
- [ ] Listo para ver diagramas UML

