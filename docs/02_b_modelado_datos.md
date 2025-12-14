# 📊 Modelado de Datos y Clases — Classroom Explorer

> **Versión**: 1.0  
> **Fecha**: 2024-12-14  
> **Autor**: Equipo de Desarrollo  
> **Estado**: 📝 En Revisión

---

## 📑 Índice

1. [Modelo de Datos Lógico](#1-modelo-de-datos-lógico)
2. [Diagrama de Clases del Backend](#2-diagrama-de-clases-del-backend)
3. [Diccionario de Datos](#3-diccionario-de-datos)

---

## 1. Modelo de Datos Lógico

### 1.1 Contexto Importante

```
⚠️ NOTA CRÍTICA: Este proyecto NO tiene base de datos propia.

• Los datos se leen directamente de Google Classroom API
• No hay persistencia local (por ahora)
• El modelo lógico representa las ENTIDADES DE DOMINIO, no tablas SQL

POR QUÉ SÍ definir un modelo lógico:
✅ Clarifica qué datos manejamos
✅ Define la estructura de las entidades de dominio (POO)
✅ Facilita agregar persistencia en el futuro (Supabase)
✅ Documenta las relaciones entre entidades
```

---

### 1.2 Diagrama Entidad-Relación (DER)

```mermaid
erDiagram
    USER ||--o{ COURSE : "teaches/enrolls"
    COURSE ||--o{ MATERIAL : "contains"
    MATERIAL }o--|| MATERIAL_TYPE : "has"
    
    USER {
        string id PK "Google User ID"
        string email "Email del usuario"
        string name "Nombre completo"
        string picture_url "URL de foto de perfil"
        datetime last_login "Última autenticación"
    }
    
    COURSE {
        string id PK "Google Course ID"
        string name "Nombre del curso"
        string section "Sección (ej: 3°A)"
        string description "Descripción del curso"
        string state "ACTIVE, ARCHIVED, PROVISIONED"
        string owner_id FK "ID del profesor"
        datetime created_at "Fecha de creación"
        datetime updated_at "Última actualización"
    }
    
    MATERIAL {
        string id PK "Google CourseWork ID"
        string course_id FK "ID del curso"
        string title "Título del material"
        string description "Descripción"
        string type "Tipo de material"
        string url "URL del recurso"
        datetime created_at "Fecha de creación"
        datetime updated_at "Última actualización"
        datetime due_date "Fecha de entrega (si aplica)"
        int max_points "Puntos máximos (si es tarea)"
    }
    
    MATERIAL_TYPE {
        string code PK "pdf, video, document, etc."
        string label "Etiqueta legible"
        string icon "Icono asociado"
    }
```

---

### 1.3 Descripción de Entidades

#### 🧑 **USER (Usuario)**

```
DESCRIPCIÓN:
Representa un usuario de Google Classroom (profesor o estudiante).

FUENTE DE DATOS:
• Google OAuth 2.0 (perfil del usuario)
• Google Classroom API (roles)

CICLO DE VIDA:
• Se crea al hacer login por primera vez
• Se actualiza en cada autenticación
• No se persiste localmente (por ahora)

RELACIONES:
• Un USER puede tener múltiples COURSES (como profesor o estudiante)
```

| Atributo | Tipo | Obligatorio | Descripción |
|----------|------|-------------|-------------|
| `id` | string | ✅ | ID único de Google (sub del JWT) |
| `email` | string | ✅ | Email de Google |
| `name` | string | ✅ | Nombre completo |
| `picture_url` | string | ❌ | URL de la foto de perfil |
| `last_login` | datetime | ✅ | Timestamp de última autenticación |

---

#### 📚 **COURSE (Curso)**

```
DESCRIPCIÓN:
Representa un curso de Google Classroom.

FUENTE DE DATOS:
• Google Classroom API: courses.list

CICLO DE VIDA:
• Se obtiene de Google API en cada request
• No se persiste localmente
• Se cachea en memoria durante la sesión (5 min)

RELACIONES:
• Un COURSE pertenece a un USER (owner)
• Un COURSE contiene múltiples MATERIALS
```

| Atributo | Tipo | Obligatorio | Descripción |
|----------|------|-------------|-------------|
| `id` | string | ✅ | ID único de Google Classroom |
| `name` | string | ✅ | Nombre del curso (ej: "Matemáticas 3°A") |
| `section` | string | ❌ | Sección o división |
| `description` | string | ❌ | Descripción del curso |
| `state` | string | ✅ | ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED |
| `owner_id` | string | ✅ | ID del profesor propietario |
| `created_at` | datetime | ✅ | Fecha de creación en Classroom |
| `updated_at` | datetime | ✅ | Última actualización |

**Reglas de Negocio:**
- ✅ Solo cursos con `state = ACTIVE` se muestran por defecto
- ✅ El `name` es obligatorio y debe tener al menos 3 caracteres
- ✅ Un curso sin materiales es válido (curso nuevo)

---

#### 📄 **MATERIAL (Material)**

```
DESCRIPCIÓN:
Representa un material/recurso de un curso (tarea, archivo, video, link, etc.).

FUENTE DE DATOS:
• Google Classroom API: courses.courseWork.list
• Google Classroom API: courses.courseWorkMaterials.list

CICLO DE VIDA:
• Se obtiene de Google API al seleccionar un curso
• No se persiste localmente
• Se cachea en memoria durante la sesión

RELACIONES:
• Un MATERIAL pertenece a un COURSE
• Un MATERIAL tiene un MATERIAL_TYPE
```

| Atributo | Tipo | Obligatorio | Descripción |
|----------|------|-------------|-------------|
| `id` | string | ✅ | ID único de Google Classroom |
| `course_id` | string | ✅ | ID del curso al que pertenece |
| `title` | string | ✅ | Título del material |
| `description` | string | ❌ | Descripción detallada |
| `type` | string | ✅ | Tipo: pdf, video, document, link, form, etc. |
| `url` | string | ✅ | URL para abrir el recurso |
| `created_at` | datetime | ✅ | Fecha de creación |
| `updated_at` | datetime | ✅ | Última actualización |
| `due_date` | datetime | ❌ | Fecha de entrega (solo si es tarea) |
| `max_points` | int | ❌ | Puntos máximos (solo si es tarea) |

**Reglas de Negocio:**
- ✅ El `title` es obligatorio
- ✅ El `url` debe ser una URL válida (http/https)
- ✅ El `type` debe ser uno de los valores del enum MaterialType
- ✅ Si `due_date` existe, debe ser posterior a `created_at`

---

#### 🏷️ **MATERIAL_TYPE (Tipo de Material)**

```
DESCRIPCIÓN:
Catálogo de tipos de materiales soportados.

FUENTE DE DATOS:
• Definido en código (enum)
• No viene de Google API

CICLO DE VIDA:
• Valores fijos en el código
• Se usa para clasificar materiales
```

| Código | Etiqueta | Icono | Descripción |
|--------|----------|-------|-------------|
| `pdf` | PDF | 📄 | Documento PDF |
| `video` | Video | 🎥 | Video (YouTube, Drive) |
| `document` | Documento | 📝 | Google Docs, Word, etc. |
| `link` | Enlace | 🔗 | URL externa |
| `form` | Formulario | 📋 | Google Forms |
| `image` | Imagen | 🖼️ | JPG, PNG, GIF |
| `assignment` | Tarea | ✏️ | Tarea con entrega |
| `file` | Archivo | 📎 | Otro tipo de archivo |

---

### 1.4 Relaciones y Cardinalidad

```
┌─────────────────────────────────────────────────────────────────┐
│                    RELACIONES ENTRE ENTIDADES                   │
└─────────────────────────────────────────────────────────────────┘

1. USER ──< COURSE (1:N)
   ────────────────────────────────────────────────────────────
   • Un usuario puede tener múltiples cursos
   • Un curso pertenece a un solo usuario (owner)
   
   Implementación:
   • Course.owner_id → User.id (Foreign Key conceptual)

2. COURSE ──< MATERIAL (1:N)
   ────────────────────────────────────────────────────────────
   • Un curso puede tener múltiples materiales
   • Un material pertenece a un solo curso
   
   Implementación:
   • Material.course_id → Course.id (Foreign Key conceptual)

3. MATERIAL >── MATERIAL_TYPE (N:1)
   ────────────────────────────────────────────────────────────
   • Múltiples materiales pueden tener el mismo tipo
   • Un material tiene un solo tipo
   
   Implementación:
   • Material.type → MaterialType.code (Enum)
```

---

### 1.5 Modelo Lógico vs. Modelo Físico

```
┌─────────────────────────────────────────────────────────────────┐
│  IMPORTANTE: Este es el MODELO LÓGICO (conceptual)              │
│  ─────────────────────────────────────────────────────────────  │
│  • Define QUÉ datos manejamos                                   │
│  • Define CÓMO se relacionan                                    │
│  • NO define tablas SQL (no hay DB propia)                      │
│                                                                 │
│  Si en el futuro agregamos Supabase:                            │
│  • Este modelo se convierte en el diseño de tablas              │
│  • Agregamos índices, constraints, triggers                     │
│  • Por ahora, solo guía nuestras entidades de dominio           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Diagrama de Clases del Backend

### 2.1 Arquitectura de Clases Completa

```mermaid
classDiagram
    %% ═══════════════════════════════════════════════════════════
    %% DOMAIN LAYER - Entidades
    %% ═══════════════════════════════════════════════════════════
    
    class Course {
        +string id
        +string name
        +string section
        +string description
        +CourseState state
        +string owner_id
        +datetime created_at
        +datetime updated_at
        +__init__(id, name, section, state, owner_id, created_at, updated_at)
        +is_active() bool
        +to_dict() dict
    }
    
    class Material {
        +string id
        +string course_id
        +string title
        +string description
        +MaterialType type
        +string url
        +datetime created_at
        +datetime updated_at
        +datetime due_date
        +int max_points
        +__init__(id, course_id, title, type, url, created_at)
        +is_overdue() bool
        +has_due_date() bool
        +to_dict() dict
    }
    
    class MaterialType {
        <<enumeration>>
        PDF
        VIDEO
        DOCUMENT
        LINK
        FORM
        IMAGE
        ASSIGNMENT
        FILE
        +get_icon() string
        +get_label() string
    }
    
    class CourseState {
        <<enumeration>>
        ACTIVE
        ARCHIVED
        PROVISIONED
        DECLINED
        SUSPENDED
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% DOMAIN LAYER - Interfaces (Ports)
    %% ═══════════════════════════════════════════════════════════
    
    class ClassroomRepository {
        <<interface>>
        +get_user_courses(user_id: string) List~Course~
        +get_course_materials(course_id: string) List~Material~
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% DOMAIN LAYER - Factories
    %% ═══════════════════════════════════════════════════════════
    
    class MaterialFactory {
        <<factory>>
        +create(id, title, type, url, course_id, created_at) Material
        +create_from_dict(data: dict) Material
        -_validate_url(url: string) bool
    }
    
    class CourseFactory {
        <<factory>>
        +create(id, name, section, state, owner_id, created_at) Course
        +create_from_dict(data: dict) Course
        -_validate_name(name: string) bool
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% APPLICATION LAYER - Use Cases
    %% ═══════════════════════════════════════════════════════════
    
    class ListUserCoursesUseCase {
        -ClassroomRepository repository
        +__init__(repository: ClassroomRepository)
        +execute(user_id: string) List~Course~
    }
    
    class ListCourseMaterialsUseCase {
        -ClassroomRepository repository
        +__init__(repository: ClassroomRepository)
        +execute(course_id: string) List~Material~
    }
    
    class FilterMaterialsUseCase {
        +execute(materials: List~Material~, filters: List~MaterialFilterStrategy~) List~Material~
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% APPLICATION LAYER - Filters (Strategy Pattern)
    %% ═══════════════════════════════════════════════════════════
    
    class MaterialFilterStrategy {
        <<interface>>
        +filter(materials: List~Material~) List~Material~
    }
    
    class FilterByType {
        -MaterialType material_type
        +__init__(material_type: MaterialType)
        +filter(materials: List~Material~) List~Material~
    }
    
    class FilterByDateRange {
        -datetime start_date
        -datetime end_date
        +__init__(start_date, end_date)
        +filter(materials: List~Material~) List~Material~
    }
    
    class FilterByCourse {
        -string course_id
        +__init__(course_id: string)
        +filter(materials: List~Material~) List~Material~
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% INFRASTRUCTURE LAYER - Repositories
    %% ═══════════════════════════════════════════════════════════
    
    class GoogleClassroomRepository {
        -GoogleClassroomClient client
        -ClassroomMapper mapper
        +__init__(client: GoogleClassroomClient)
        +get_user_courses(user_id: string) List~Course~
        +get_course_materials(course_id: string) List~Material~
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% INFRASTRUCTURE LAYER - HTTP Client
    %% ═══════════════════════════════════════════════════════════
    
    class GoogleClassroomClient {
        <<singleton>>
        -Session session
        -string base_url
        +list_courses(access_token: string) dict
        +list_course_work(course_id: string, access_token: string) dict
        +list_course_work_materials(course_id: string, access_token: string) dict
        -_make_request(method, url, headers, max_retries) dict
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% INFRASTRUCTURE LAYER - Mappers (Adapter Pattern)
    %% ═══════════════════════════════════════════════════════════
    
    class ClassroomMapper {
        +api_course_to_domain(api_data: dict) Course
        +api_material_to_domain(api_data: dict) Material
        -_detect_material_type(api_data: dict) MaterialType
        -_extract_material_url(api_data: dict, type: MaterialType) string
        -_parse_google_timestamp(timestamp: string) datetime
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% INFRASTRUCTURE LAYER - Configuration
    %% ═══════════════════════════════════════════════════════════
    
    class Config {
        <<singleton>>
        +string GOOGLE_CLIENT_ID
        +string GOOGLE_CLIENT_SECRET
        +string OAUTH_REDIRECT_URI
        +string APP_URL
        +string SESSION_SECRET
        +string ENVIRONMENT
        +validate() void
        +is_production() bool
    }
    
    %% ═══════════════════════════════════════════════════════════
    %% RELACIONES
    %% ═══════════════════════════════════════════════════════════
    
    %% Domain relationships
    Material --> MaterialType : has
    Material --> Course : belongs to
    Course --> CourseState : has
    
    %% Factory relationships
    MaterialFactory ..> Material : creates
    CourseFactory ..> Course : creates
    
    %% Use Case relationships
    ListUserCoursesUseCase --> ClassroomRepository : uses
    ListCourseMaterialsUseCase --> ClassroomRepository : uses
    FilterMaterialsUseCase --> MaterialFilterStrategy : uses
    
    %% Strategy relationships
    MaterialFilterStrategy <|.. FilterByType : implements
    MaterialFilterStrategy <|.. FilterByDateRange : implements
    MaterialFilterStrategy <|.. FilterByCourse : implements
    
    %% Repository relationships
    ClassroomRepository <|.. GoogleClassroomRepository : implements
    GoogleClassroomRepository --> GoogleClassroomClient : uses
    GoogleClassroomRepository --> ClassroomMapper : uses
    
    %% Mapper relationships
    ClassroomMapper ..> Course : creates
    ClassroomMapper ..> Material : creates
    ClassroomMapper --> CourseFactory : uses
    ClassroomMapper --> MaterialFactory : uses
```

---

### 2.2 Diagrama de Clases por Capa

#### 📦 Domain Layer (Núcleo)

```mermaid
classDiagram
    class Course {
        +string id
        +string name
        +string section
        +string description
        +CourseState state
        +string owner_id
        +datetime created_at
        +datetime updated_at
        +__init__(...)
        +is_active() bool
        +to_dict() dict
        +__str__() string
        +__repr__() string
    }
    
    class Material {
        +string id
        +string course_id
        +string title
        +string description
        +MaterialType type
        +string url
        +datetime created_at
        +datetime updated_at
        +datetime due_date
        +int max_points
        +__init__(...)
        +is_overdue() bool
        +has_due_date() bool
        +is_assignment() bool
        +to_dict() dict
        +__str__() string
    }
    
    class MaterialType {
        <<enumeration>>
        PDF = "pdf"
        VIDEO = "video"
        DOCUMENT = "document"
        LINK = "link"
        FORM = "form"
        IMAGE = "image"
        ASSIGNMENT = "assignment"
        FILE = "file"
        +get_icon() string
        +get_label() string
    }
    
    class CourseState {
        <<enumeration>>
        ACTIVE = "ACTIVE"
        ARCHIVED = "ARCHIVED"
        PROVISIONED = "PROVISIONED"
        DECLINED = "DECLINED"
        SUSPENDED = "SUSPENDED"
    }
    
    Material --> MaterialType
    Material --> Course
    Course --> CourseState
```

**Características Clave:**
- ✅ **Sin dependencias externas**: Solo Python estándar
- ✅ **Inmutables**: Usar `@dataclass(frozen=True)` cuando sea posible
- ✅ **Validaciones**: En `__post_init__` o en Factory
- ✅ **Métodos de negocio**: `is_active()`, `is_overdue()`, etc.

---

#### ⚙️ Application Layer (Casos de Uso)

```mermaid
classDiagram
    class ListUserCoursesUseCase {
        -ClassroomRepository repository
        +__init__(repository: ClassroomRepository)
        +execute(user_id: string) List~Course~
    }
    
    class ListCourseMaterialsUseCase {
        -ClassroomRepository repository
        +__init__(repository: ClassroomRepository)
        +execute(course_id: string) List~Material~
    }
    
    class FilterMaterialsUseCase {
        +execute(materials: List~Material~, filters: List~MaterialFilterStrategy~) List~Material~
        -_apply_filters(materials, filters) List~Material~
    }
    
    class MaterialFilterStrategy {
        <<interface>>
        +filter(materials: List~Material~) List~Material~
    }
    
    class FilterByType {
        -MaterialType material_type
        +filter(materials: List~Material~) List~Material~
    }
    
    class FilterByDateRange {
        -datetime start_date
        -datetime end_date
        +filter(materials: List~Material~) List~Material~
    }
    
    class FilterByCourse {
        -string course_id
        +filter(materials: List~Material~) List~Material~
    }
    
    ListUserCoursesUseCase --> ClassroomRepository
    ListCourseMaterialsUseCase --> ClassroomRepository
    FilterMaterialsUseCase --> MaterialFilterStrategy
    MaterialFilterStrategy <|.. FilterByType
    MaterialFilterStrategy <|.. FilterByDateRange
    MaterialFilterStrategy <|.. FilterByCourse
```

**Características Clave:**
- ✅ **Un caso de uso = Una acción del usuario**
- ✅ **Reciben dependencias por constructor** (DI)
- ✅ **Método `execute()`** como punto de entrada
- ✅ **Sin lógica de infraestructura** (HTTP, DB, etc.)

---

#### 🔧 Infrastructure Layer (Adaptadores)

```mermaid
classDiagram
    class ClassroomRepository {
        <<interface>>
        +get_user_courses(user_id: string) List~Course~
        +get_course_materials(course_id: string) List~Material~
    }
    
    class GoogleClassroomRepository {
        -GoogleClassroomClient client
        -ClassroomMapper mapper
        +__init__(client: GoogleClassroomClient)
        +get_user_courses(user_id: string) List~Course~
        +get_course_materials(course_id: string) List~Material~
        -_fetch_course_work(course_id, token) dict
        -_fetch_course_work_materials(course_id, token) dict
    }
    
    class GoogleClassroomClient {
        <<singleton>>
        -Session session
        -string base_url
        -_instance GoogleClassroomClient
        +__new__() GoogleClassroomClient
        +list_courses(access_token: string) dict
        +list_course_work(course_id, access_token) dict
        +list_course_work_materials(course_id, access_token) dict
        -_make_request(method, url, headers, max_retries) dict
        -_handle_rate_limit(response) void
    }
    
    class ClassroomMapper {
        +api_course_to_domain(api_data: dict) Course
        +api_material_to_domain(api_data: dict) Material
        -_detect_material_type(api_data: dict) MaterialType
        -_extract_material_url(api_data, type) string
        -_parse_google_timestamp(timestamp: string) datetime
    }
    
    class Config {
        <<singleton>>
        +string GOOGLE_CLIENT_ID
        +string GOOGLE_CLIENT_SECRET
        +string OAUTH_REDIRECT_URI
        +string APP_URL
        +string SESSION_SECRET
        +string ENVIRONMENT
        +validate() void
        +is_production() bool
        -_load_from_env() void
    }
    
    ClassroomRepository <|.. GoogleClassroomRepository
    GoogleClassroomRepository --> GoogleClassroomClient
    GoogleClassroomRepository --> ClassroomMapper
    GoogleClassroomClient --> Config
```

**Características Clave:**
- ✅ **Implementa interfaces del Domain**
- ✅ **Conoce detalles de Google API**
- ✅ **Maneja errores de red**
- ✅ **Convierte formatos externos → Domain**

---

### 2.3 Diagrama de Secuencia: Listar Cursos

```mermaid
sequenceDiagram
    actor Usuario
    participant Frontend
    participant API as API Endpoint
    participant UseCase as ListUserCoursesUseCase
    participant Repo as GoogleClassroomRepository
    participant Client as GoogleClassroomClient
    participant Mapper as ClassroomMapper
    participant Google as Google Classroom API
    
    Usuario->>Frontend: Click "Ver mis cursos"
    Frontend->>API: GET /api/courses
    
    Note over API: Valida token de sesión
    
    API->>UseCase: execute(user_id)
    UseCase->>Repo: get_user_courses(user_id)
    
    Repo->>Client: list_courses(access_token)
    Client->>Google: GET /v1/courses
    
    alt Respuesta exitosa
        Google-->>Client: 200 OK + JSON
        Client-->>Repo: dict (API response)
        
        loop Para cada curso en la respuesta
            Repo->>Mapper: api_course_to_domain(course_data)
            Mapper-->>Repo: Course (entidad)
        end
        
        Repo-->>UseCase: List[Course]
        UseCase-->>API: List[Course]
        
        Note over API: Serializa a JSON
        
        API-->>Frontend: 200 OK + JSON
        Frontend-->>Usuario: Muestra lista de cursos
    
    else Error de API
        Google-->>Client: 500 Error
        Client->>Client: Reintentar (backoff)
        
        alt Reintento exitoso
            Google-->>Client: 200 OK
        else Fallo definitivo
            Client-->>Repo: GoogleAPIError
            Repo-->>UseCase: GoogleAPIError
            UseCase-->>API: GoogleAPIError
            API-->>Frontend: 500 + mensaje de error
            Frontend-->>Usuario: "Error al cargar cursos"
        end
    end
```

---

### 2.4 Diagrama de Secuencia: Filtrar Materiales

```mermaid
sequenceDiagram
    actor Usuario
    participant Frontend
    participant API as API Endpoint
    participant UseCase as FilterMaterialsUseCase
    participant Strategy1 as FilterByType
    participant Strategy2 as FilterByDateRange
    
    Usuario->>Frontend: Selecciona filtros (PDF, última semana)
    Frontend->>API: GET /api/materials?type=pdf&start_date=2024-12-07
    
    Note over API: Obtiene materiales (ya cargados)
    
    API->>API: Construir estrategias de filtrado
    API->>Strategy1: new FilterByType(MaterialType.PDF)
    API->>Strategy2: new FilterByDateRange(start, end)
    
    API->>UseCase: execute(materials, [Strategy1, Strategy2])
    
    UseCase->>Strategy1: filter(materials)
    Strategy1-->>UseCase: materials_filtrados_por_tipo
    
    UseCase->>Strategy2: filter(materials_filtrados_por_tipo)
    Strategy2-->>UseCase: materiales_finales
    
    UseCase-->>API: List[Material] (filtrados)
    
    Note over API: Serializa a JSON
    
    API-->>Frontend: 200 OK + JSON
    Frontend-->>Usuario: Muestra 5 PDFs de la última semana
```

---

## 3. Diccionario de Datos

### 3.1 Entidad: Course

| Atributo | Tipo Python | Tipo Lógico | Nullable | Default | Validación |
|----------|-------------|-------------|----------|---------|------------|
| `id` | `str` | string(255) | ❌ | - | Regex: `^[0-9]+$` |
| `name` | `str` | string(500) | ❌ | - | len >= 3 |
| `section` | `str \| None` | string(100) | ✅ | None | - |
| `description` | `str \| None` | text | ✅ | None | - |
| `state` | `CourseState` | enum | ❌ | ACTIVE | Enum values |
| `owner_id` | `str` | string(255) | ❌ | - | Regex: `^[0-9]+$` |
| `created_at` | `datetime` | timestamp | ❌ | - | - |
| `updated_at` | `datetime` | timestamp | ❌ | - | >= created_at |

**Índices Recomendados (si se persiste):**
- PRIMARY KEY: `id`
- INDEX: `owner_id`
- INDEX: `state`

---

### 3.2 Entidad: Material

| Atributo | Tipo Python | Tipo Lógico | Nullable | Default | Validación |
|----------|-------------|-------------|----------|---------|------------|
| `id` | `str` | string(255) | ❌ | - | Regex: `^[0-9]+$` |
| `course_id` | `str` | string(255) | ❌ | - | FK a Course.id |
| `title` | `str` | string(500) | ❌ | - | len >= 1 |
| `description` | `str \| None` | text | ✅ | None | - |
| `type` | `MaterialType` | enum | ❌ | - | Enum values |
| `url` | `str` | string(2048) | ❌ | - | Regex: `^https?://` |
| `created_at` | `datetime` | timestamp | ❌ | - | - |
| `updated_at` | `datetime` | timestamp | ❌ | - | >= created_at |
| `due_date` | `datetime \| None` | timestamp | ✅ | None | > created_at |
| `max_points` | `int \| None` | integer | ✅ | None | >= 0 |

**Índices Recomendados (si se persiste):**
- PRIMARY KEY: `id`
- INDEX: `course_id`
- INDEX: `type`
- INDEX: `created_at`

---

### 3.3 Enum: MaterialType

| Valor | Código | Descripción | Icono | Color Sugerido |
|-------|--------|-------------|-------|----------------|
| PDF | `"pdf"` | Documento PDF | 📄 | #E74C3C (rojo) |
| VIDEO | `"video"` | Video (YouTube, Drive) | 🎥 | #9B59B6 (púrpura) |
| DOCUMENT | `"document"` | Google Docs, Word | 📝 | #3498DB (azul) |
| LINK | `"link"` | Enlace externo | 🔗 | #1ABC9C (turquesa) |
| FORM | `"form"` | Google Forms | 📋 | #F39C12 (naranja) |
| IMAGE | `"image"` | JPG, PNG, GIF | 🖼️ | #E67E22 (naranja oscuro) |
| ASSIGNMENT | `"assignment"` | Tarea con entrega | ✏️ | #2ECC71 (verde) |
| FILE | `"file"` | Otro archivo | 📎 | #95A5A6 (gris) |

---

### 3.4 Enum: CourseState

| Valor | Código | Descripción |
|-------|--------|-------------|
| ACTIVE | `"ACTIVE"` | Curso activo y visible |
| ARCHIVED | `"ARCHIVED"` | Curso archivado (no visible por defecto) |
| PROVISIONED | `"PROVISIONED"` | Curso creado pero no activado |
| DECLINED | `"DECLINED"` | Invitación rechazada |
| SUSPENDED | `"SUSPENDED"` | Curso suspendido |

---

## 📎 Resumen Ejecutivo

### Decisiones de Modelado

| Decisión | Justificación |
|----------|---------------|
| **No persistencia local** | Datos vienen de Google API en tiempo real |
| **Modelo lógico definido** | Facilita agregar DB en el futuro |
| **Entidades inmutables** | Usar `@dataclass(frozen=True)` para seguridad |
| **Enums para tipos** | Evita strings mágicos, autocomplete en IDE |
| **Validaciones en Factory** | Centraliza reglas de creación |

### Próximo Paso

Una vez aprobado este documento, pasaremos a:
- **Parte C**: Diagramas de componentes y mapa de endpoints

---

## ✅ Checklist de Aprobación

- [ ] Modelo de datos lógico revisado
- [ ] Entidades y relaciones claras
- [ ] Diagrama de clases completo
- [ ] Diagramas de secuencia entendidos
- [ ] Diccionario de datos aprobado
- [ ] Listo para ver mapa de endpoints
