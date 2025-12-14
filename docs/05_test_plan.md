# 📋 Plan de Pruebas — Classroom Explorer

**Versión:** 1.0  
**Fecha:** 2025-12-14  
**Fase:** 5 (QA Formal y Automatizado)

---

## 📖 Regla de Evolución

> Durante la construcción, las pruebas vivían dentro del archivo (`__main__`).  
> Ahora que el código es estable, las pruebas migran a archivos dedicados (`tests/`).

---

## 🗂️ Estructura de Tests

```
tests/
├── __init__.py
├── conftest.py           → Fixtures compartidas
├── test_domain.py        → Entidades y Value Objects
├── test_factories.py     → Factories
├── test_infrastructure.py → Config, Cache, Mapper
├── test_use_cases.py     → Application Layer
├── test_routes.py        → API Handlers
└── test_integration.py   → Flujos completos
```

---

## 📊 Casos de Prueba

### Domain Layer (HU-001: Visualizar Cursos)

| ID | Test | Criterio Aceptación | Archivo |
|----|------|---------------------|---------|
| T-D01 | MaterialType.from_string válido | CA-001.1 | test_domain.py |
| T-D02 | MaterialType.from_string inválido | CA-001.2 | test_domain.py |
| T-D03 | CourseState.is_active() | CA-001.3 | test_domain.py |
| T-D04 | Course entity creation | CA-001.4 | test_domain.py |
| T-D05 | Course.to_dict() serialization | CA-001.5 | test_domain.py |
| T-D06 | Material entity creation | CA-002.1 | test_domain.py |
| T-D07 | Material.is_overdue() | CA-002.2 | test_domain.py |

### Factories (HU-001)

| ID | Test | Criterio Aceptación | Archivo |
|----|------|---------------------|---------|
| T-F01 | CourseFactory.create() | CA-001.6 | test_factories.py |
| T-F02 | CourseFactory.create_from_dict() | CA-001.7 | test_factories.py |
| T-F03 | MaterialFactory.create() | CA-002.3 | test_factories.py |
| T-F04 | MaterialFactory con tipo inválido | CA-002.4 | test_factories.py |

### Infrastructure (HU-003: Rendimiento)

| ID | Test | Criterio Aceptación | Archivo |
|----|------|---------------------|---------|
| T-I01 | Config carga variables | CA-003.1 | test_infrastructure.py |
| T-I02 | Config.validate() sin vars | CA-003.2 | test_infrastructure.py |
| T-I03 | MemoryCache set/get | CA-003.3 | test_infrastructure.py |
| T-I04 | MemoryCache TTL expiration | CA-003.4 | test_infrastructure.py |
| T-I05 | ClassroomMapper.to_course() | CA-003.5 | test_infrastructure.py |

### Use Cases (HU-002: Filtrar Materiales)

| ID | Test | Criterio Aceptación | Archivo |
|----|------|---------------------|---------|
| T-U01 | ListUserCourses.execute() | CA-002.1 | test_use_cases.py |
| T-U02 | ListUserCourses con filtro | CA-002.2 | test_use_cases.py |
| T-U03 | ListCourseMaterials.execute() | CA-002.3 | test_use_cases.py |
| T-U04 | ListCourseMaterials por tipo | CA-002.4 | test_use_cases.py |

### Routes (HU-004: Autenticación)

| ID | Test | Criterio Aceptación | Archivo |
|----|------|---------------------|---------|
| T-R01 | AuthHandler hereda BaseHTTPRequestHandler | CA-004.1 | test_routes.py |
| T-R02 | SessionStore create/get | CA-004.2 | test_routes.py |
| T-R03 | CoursesHandler existe | CA-004.3 | test_routes.py |
| T-R04 | MaterialsHandler existe | CA-004.4 | test_routes.py |

### Integration (HU-000: Setup)

| ID | Test | Criterio Aceptación | Archivo |
|----|------|---------------------|---------|
| T-INT01 | MainRouter hereda correctly | CA-000.1 | test_integration.py |
| T-INT02 | VercelBridge callable | CA-000.2 | test_integration.py |
| T-INT03 | app variable expuesta | CA-000.3 | test_integration.py |

---

## 🚀 Comandos de Ejecución

```powershell
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ -v --cov=api --cov-report=html

# Solo un archivo
pytest tests/test_domain.py -v
```

---

## 🤖 AI Stack

Generado mediante metodología SDLC V5 usando Google Antigravity + Claude Opus 4.5
