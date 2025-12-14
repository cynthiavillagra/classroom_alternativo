# 🛠️ Manual Técnico del Backend — Classroom Explorer

> **Versión**: 1.0  
> **Fecha**: 2024-12-14  
> **Autor**: Equipo de Desarrollo  
> **Estado**: 🚧 En Construcción

---

## 📑 Índice

1. [Setup de Entorno Local](#1-setup-de-entorno-local)
2. [Archivos de Configuración](#2-archivos-de-configuración)
3. [Domain Layer (POO Pura)](#3-domain-layer-poo-pura)
4. [Infrastructure Layer](#4-infrastructure-layer)
5. [Application Layer](#5-application-layer)
6. [API Layer](#6-api-layer)

---

## 1. Setup de Entorno Local

### 1.1 Prerrequisitos

- Python 3.11 o superior
- Git
- Editor de código (VS Code recomendado)

### 1.2 Pasos de Instalación

```powershell
# 1. Clonar el repositorio
git clone <tu-repo-url>
cd "app classroom"

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual (Windows)
.\venv\Scripts\activate

# 4. Actualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Verificar instalación
pip list
```

### 1.3 Configurar Variables de Entorno

```powershell
# Copiar plantilla
cp .env.example .env

# Editar .env con tus credenciales
# (Ver sección "Obtener Credenciales de Google" en README.md)
```

---

## 2. Archivos de Configuración

### 2.1 requirements.txt

**Archivo:** `requirements.txt`

**Propósito:** Define todas las dependencias Python del proyecto

**Trazabilidad:** RNF-MANT04 (Convenciones de código), Setup inicial

#### 📝 Contenido

```txt
# Framework Web
flask==3.0.0
werkzeug==3.0.1

# Autenticación y Seguridad
PyJWT==2.8.0
cryptography==41.0.7

# HTTP Client
requests==2.31.0
google-auth==2.25.2
google-auth-oauthlib==1.2.0

# Validación de Datos
pydantic==2.5.3

# Utilidades
python-dotenv==1.0.0

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
```

#### ✅ POR QUÉ SÍ estas dependencias

| Dependencia | Justificación |
|-------------|---------------|
| **Flask** | Framework web ligero, compatible con Vercel Serverless |
| **PyJWT** | Estándar de la industria para JWT, simple y seguro |
| **requests** | Cliente HTTP más usado en Python, simple y confiable |
| **google-auth** | Librería oficial de Google, maneja OAuth 2.0 correctamente |
| **pydantic** | Validación de datos con type hints, previene errores en runtime |
| **python-dotenv** | Carga variables de .env automáticamente en desarrollo |
| **pytest** | Framework de testing más popular en Python |

#### ❌ POR QUÉ NO otras alternativas

| Alternativa | Por Qué NO |
|-------------|------------|
| **Django** | Demasiado pesado para serverless, tiene ORM que no necesitamos |
| **FastAPI** | Excelente, pero más complejo para aprender (async/await) |
| **urllib** | Más bajo nivel que requests, menos legible |

#### 🎓 CONCEPTOS EDUCATIVOS

**¿Qué es requirements.txt?**
- Es el estándar de Python para declarar dependencias
- Similar a `package.json` en Node.js
- Permite reproducir el entorno exacto en cualquier máquina

**¿Por qué versiones fijas (==)?**
- ✅ **Reproducibilidad**: Todos instalan las mismas versiones
- ✅ **Estabilidad**: Evita que updates rompan el código
- ❌ **Trade-off**: No obtenemos bugfixes automáticos

---

### 2.2 README.md

**Archivo:** `README.md`

**Propósito:** Documentación principal del proyecto, punto de entrada para nuevos desarrolladores

**Trazabilidad:** RNF-MANT02 (Código documentado), Onboarding

#### ✅ POR QUÉ SÍ este README

| Sección | Justificación |
|---------|---------------|
| **Características** | Usuario entiende qué hace la app en 10 segundos |
| **Arquitectura** | Desarrollador ve que es un proyecto serio (Clean Architecture) |
| **Setup paso a paso** | Cualquiera puede replicar el entorno local |
| **Credenciales Google** | Paso más difícil, explicado en detalle |
| **Estructura de carpetas** | Mapa mental del proyecto |

#### 🎓 CONCEPTOS EDUCATIVOS

**¿Qué hace un buen README?**
1. **Responde "¿Qué es esto?"** en los primeros 3 segundos
2. **Setup funcional** — Alguien nuevo puede ejecutar la app en < 10 minutos
3. **Arquitectura visible** — Muestra que hay pensamiento detrás
4. **Troubleshooting** — Anticipa problemas comunes

---

### 2.3 vercel.json

**Archivo:** `vercel.json`

**Propósito:** Configuración de deploy en Vercel (plataforma serverless)

**Trazabilidad:** RNF-PERF02 (Respuesta de API), Deploy en producción

#### 📝 Contenido Clave

```json
{
  "builds": [
    {"src": "api/**/*.py", "use": "@vercel/python"},
    {"src": "public/**", "use": "@vercel/static"}
  ],
  "functions": {
    "api/**/*.py": {
      "memory": 1024,
      "maxDuration": 10
    }
  }
}
```

#### ✅ POR QUÉ SÍ esta configuración

| Configuración | Justificación |
|---------------|---------------|
| **`@vercel/python`** | Builder oficial para Python serverless |
| **`memory: 1024`** | 1GB es suficiente para llamadas HTTP a Google API |
| **`maxDuration: 10`** | 10 segundos máximo (plan gratuito de Vercel) |
| **CORS headers** | Permite que el frontend llame a la API |

#### 🎓 CONCEPTOS EDUCATIVOS

**¿Qué es Vercel Serverless?**
- **Serverless** = No gestionas servidores, Vercel lo hace por ti
- **Functions** = Cada endpoint es una función independiente
- **Cold Start** = Primera llamada es lenta (~1-2s), luego es rápida
- **Stateless** = No hay estado entre requests

**CORS (Cross-Origin Resource Sharing):**
```
PROBLEMA:
• Frontend y API en el mismo dominio
• Navegador puede bloquear por seguridad

SOLUCIÓN:
• Header: Access-Control-Allow-Origin: *
• Permite requests desde cualquier origen

⚠️ EN PRODUCCIÓN:
• Cambiar a tu dominio específico
• Más seguro
```

---

### 2.4 api/domain/entities/__init__.py

**Archivo:** `api/domain/entities/__init__.py`

**Propósito:** Convierte la carpeta `entities` en un módulo Python

**Trazabilidad:** RNF-MANT04 (Convenciones de código), Estructura modular

#### 📝 Contenido

```python
from .course import Course
from .material import Material
from .material_type import MaterialType
from .course_state import CourseState

__all__ = [
    "Course",
    "Material",
    "MaterialType",
    "CourseState",
]
```

#### ✅ POR QUÉ SÍ este patrón

| Práctica | Justificación |
|----------|---------------|
| **`__all__`** | Define qué se exporta con `from entities import *` |
| **Imports relativos** | `from .course import Course` (más limpio) |
| **Documentación** | Docstring explica el propósito del paquete |

#### 🎓 CONCEPTOS EDUCATIVOS

**¿Qué es `__init__.py`?**
- Archivo especial que Python busca para reconocer un paquete
- Se ejecuta cuando importas el paquete
- Puede estar vacío o contener código de inicialización

**Ejemplo de uso:**

```python
# ❌ SIN __init__.py con exports
from api.domain.entities.course import Course
from api.domain.entities.material import Material

# ✅ CON __init__.py con exports
from api.domain.entities import Course, Material
```

**¿Qué es `__all__`?**
- Controla qué se exporta con `from module import *`
- Documentación explícita de la API pública
- IDEs usan esta info para autocomplete

---

## 3. Domain Layer (POO Pura)

### 3.1 MaterialType (Enum)

**Archivo:** `api/domain/entities/material_type.py`

**Propósito:** Define los tipos de materiales soportados

**Trazabilidad:** Entidad de dominio, RF-M03 (Listar materiales)

#### 📝 Código Completo

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
```

#### ✅ POR QUÉ SÍ usar Enum

- ✅ Evita strings mágicos ("pdf", "video", etc.)
- ✅ Autocomplete en el IDE
- ✅ Type safety (el IDE detecta errores)
- ✅ Fácil de extender (agregar nuevos tipos)

#### ❌ POR QUÉ NO usar strings directamente

- ❌ Typos no se detectan hasta runtime
- ❌ No hay autocomplete
- ❌ Difícil de refactorizar

---

### 3.2 CourseState (Enum)

**Archivo:** `api/domain/entities/course_state.py`

**Propósito:** Define los estados de un curso en Google Classroom

**Trazabilidad:** Entidad de dominio, RF-M02 (Listar cursos)

#### 📝 Código Completo

```python
from enum import Enum

class CourseState(Enum):
    """Estados de un curso en Google Classroom."""
    
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    PROVISIONED = "PROVISIONED"
    DECLINED = "DECLINED"
    SUSPENDED = "SUSPENDED"
    
    def is_active(self) -> bool:
        """Verifica si el curso está activo."""
        return self == CourseState.ACTIVE
    
    def is_visible(self) -> bool:
        """Verifica si el curso debería mostrarse por defecto."""
        return self in (CourseState.ACTIVE, CourseState.ARCHIVED)
```

#### 🎓 CONCEPTOS EDUCATIVOS

**Estados oficiales de Google Classroom API:**
- **ACTIVE**: Curso activo y visible
- **ARCHIVED**: Curso archivado (solo lectura)
- **PROVISIONED**: Curso creado pero no activado
- **DECLINED**: Invitación al curso rechazada
- **SUSPENDED**: Curso suspendido por el administrador

---

## 4. Infrastructure Layer

*(Sección en construcción - se completará con los próximos archivos)*

---

## 5. Application Layer

*(Sección en construcción - se completará con los próximos archivos)*

---

## 6. API Layer

*(Sección en construcción - se completará con los próximos archivos)*

---

## 📎 Resumen de Archivos Generados

| # | Archivo | Estado | Propósito |
|---|---------|--------|-----------|
| 1 | `requirements.txt` | ✅ | Dependencias Python |
| 2 | `README.md` | ✅ | Documentación principal |
| 3 | `vercel.json` | ✅ | Configuración de deploy |
| 4 | `api/domain/entities/__init__.py` | ✅ | Módulo de entidades |
| 5 | `api/domain/entities/material_type.py` | ✅ | Enum de tipos de material |
| 6 | `api/domain/entities/course_state.py` | ✅ | Enum de estados de curso |
| 7 | `api/domain/entities/course.py` | ⏳ | Entidad Course |
| 8 | `api/domain/entities/material.py` | ⏳ | Entidad Material |
| ... | ... | ⏳ | ... |

---

## ✅ Checklist de Progreso

- [x] Setup de entorno local documentado
- [x] Dependencias instaladas
- [x] Configuración de Vercel
- [x] Enums de dominio creados
- [ ] Entidades de dominio
- [ ] Factories
- [ ] Interfaces (Ports)
- [ ] Infrastructure Layer
- [ ] Application Layer
- [ ] API Layer

---

**Nota:** Este manual se actualiza automáticamente a medida que generamos cada archivo del proyecto.
