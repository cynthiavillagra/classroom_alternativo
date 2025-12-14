# 📚 Índice de Manuales Técnicos — Classroom Explorer

> **Versión**: 1.0  
> **Fecha**: 2024-12-14  
> **Estado**: 🚧 En Construcción

---

## 📖 Cómo Usar Este Índice

Cada archivo de código tiene su propio manual técnico detallado.  
Haz clic en el enlace para ver el análisis completo.

---

## 📁 Archivos Documentados

### 1. Configuración y Setup

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 1 | `requirements.txt` | [01_requirements.md](manual/01_requirements.md) | ✅ |
| 2 | `README.md` | [02_readme.md](manual/02_readme.md) | ⏳ |
| 3 | `vercel.json` | [03_vercel_json.md](manual/03_vercel_json.md) | ⏳ |
| 4 | `.env.example` | [04_env_example.md](manual/04_env_example.md) | ⏳ |

### 2. Domain Layer - Entities

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 5 | `api/domain/entities/__init__.py` | [05_entities_init.md](manual/05_entities_init.md) | ⏳ |
| 6 | `api/domain/entities/material_type.py` | [06_material_type.md](manual/06_material_type.md) | ⏳ |
| 7 | `api/domain/entities/course_state.py` | [07_course_state.md](manual/07_course_state.md) | ⏳ |
| 8 | `api/domain/entities/course.py` | [08_course.md](manual/08_course.md) | ✅ |
| 9 | `api/domain/entities/material.py` | [09_material.md](manual/09_material.md) | ⏳ |

### 3. Domain Layer - Factories

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 10 | `api/domain/factories/__init__.py` | [10_factories_init.md](manual/10_factories_init.md) | ⏳ |
| 11 | `api/domain/factories/course_factory.py` | [11_course_factory.md](manual/11_course_factory.md) | ⏳ |
| 12 | `api/domain/factories/material_factory.py` | [12_material_factory.md](manual/12_material_factory.md) | ⏳ |

### 4. Domain Layer - Interfaces (Ports)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 13 | `api/domain/interfaces/__init__.py` | [13_interfaces_init.md](manual/13_interfaces_init.md) | ⏳ |
| 14 | `api/domain/interfaces/classroom_repository.py` | [14_classroom_repository.md](manual/14_classroom_repository.md) | ⏳ |

### 5. Infrastructure Layer

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 15 | `api/infrastructure/config.py` | [15_config.md](manual/15_config.md) | ⏳ |
| 16 | `api/infrastructure/cache.py` | [16_cache.md](manual/16_cache.md) | ⏳ |
| 17 | `api/infrastructure/google_classroom_client.py` | [17_google_client.md](manual/17_google_client.md) | ⏳ |
| 18 | `api/infrastructure/mappers/classroom_mapper.py` | [18_classroom_mapper.md](manual/18_classroom_mapper.md) | ⏳ |
| 19 | `api/infrastructure/repositories/google_classroom_repository.py` | [19_google_repository.md](manual/19_google_repository.md) | ⏳ |

### 6. Application Layer

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 20 | `api/application/use_cases/list_user_courses.py` | [20_list_courses_uc.md](manual/20_list_courses_uc.md) | ⏳ |
| 21 | `api/application/use_cases/list_course_materials.py` | [21_list_materials_uc.md](manual/21_list_materials_uc.md) | ⏳ |
| 22 | `api/application/filters/material_filter_strategy.py` | [22_filter_strategy.md](manual/22_filter_strategy.md) | ⏳ |

### 7. API Layer

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 23 | `api/routes/auth.py` | [23_auth_routes.md](manual/23_auth_routes.md) | ⏳ |
| 24 | `api/routes/courses.py` | [24_courses_routes.md](manual/24_courses_routes.md) | ⏳ |
| 25 | `api/routes/materials.py` | [25_materials_routes.md](manual/25_materials_routes.md) | ⏳ |

---

## 📊 Progreso

- **Archivos creados**: 7
- **Manuales completados**: 2
- **Progreso**: 29% (2/7)

---

## 🎯 Estructura de Cada Manual

Cada manual técnico incluye:

1. **Propósito y Trazabilidad** — Qué hace y por qué existe
2. **Código Clave** — Fragmentos importantes con explicaciones
3. **✅ POR QUÉ SÍ** — Justificación de decisiones de diseño
4. **❌ POR QUÉ NO** — Alternativas descartadas y por qué
5. **🎓 CONCEPTOS EDUCATIVOS** — Explicaciones profundas de patrones y prácticas

---

## 📖 Documentación Relacionada

- [01_planificacion_analisis.md](01_planificacion_analisis.md) — Planificación y requisitos
- [02_a_arquitectura_patrones.md](02_a_arquitectura_patrones.md) — Arquitectura Clean
- [02_b_modelado_datos.md](02_b_modelado_datos.md) — Modelo de datos
- [02_c_api_dinamica.md](02_c_api_dinamica.md) — API y endpoints
- [03_estrategia_datos.md](03_estrategia_datos.md) — Estrategia de datos

---

**Nota:** Este índice se actualiza automáticamente a medida que se generan nuevos archivos y manuales.
