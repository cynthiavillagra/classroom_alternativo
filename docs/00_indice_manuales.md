# 📚 Índice de Manuales Técnicos — Classroom Explorer

> **Versión**: 2.0  
> **Fecha**: 2024-12-14  
> **Estado**: ✅ Completo

---

## 📖 Cómo Usar Este Índice

Cada archivo de código tiene su propio manual técnico detallado.  
**Sigue la numeración para replicar el proyecto desde cero.**

---

## 📁 Secuencia de Construcción

### 1. Configuración y Setup

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 01 | `requirements.txt` | [01_requirements.md](manual/01_requirements.md) | ✅ |
| 02 | `README.md` | [02_readme.md](manual/02_readme.md) | ✅ |
| 03 | `vercel.json` | [03_vercel.md](manual/03_vercel.md) | ✅ |

### 2. Domain Layer - Entities

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 04 | `api/domain/entities/__init__.py` | [04_entities_init.md](manual/04_entities_init.md) | ✅ |
| 05 | `api/domain/entities/material_type.py` | [05_material_type.md](manual/05_material_type.md) | ✅ |
| 06 | `api/domain/entities/course_state.py` | [06_course_state.md](manual/06_course_state.md) | ✅ |
| 07 | `api/domain/entities/course.py` | [07_course.md](manual/07_course.md) | ✅ |
| 08 | `api/domain/entities/material.py` | [08_material.md](manual/08_material.md) | ✅ |

### 3. Domain Layer - Factories

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 09 | `api/domain/factories/__init__.py` | [09_factories_init.md](manual/09_factories_init.md) | ✅ |
| 10 | `api/domain/factories/course_factory.py` | [10_course_factory.md](manual/10_course_factory.md) | ✅ |
| 11 | `api/domain/factories/material_factory.py` | [11_material_factory.md](manual/11_material_factory.md) | ✅ |

### 4. Domain Layer - Interfaces (Ports)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 12 | `api/domain/interfaces/__init__.py` | [12_interfaces_init.md](manual/12_interfaces_init.md) | ✅ |
| 13 | `api/domain/interfaces/classroom_repository.py` | [13_classroom_repository.md](manual/13_classroom_repository.md) | ✅ |

### 5. Infrastructure Layer

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 14 | `api/infrastructure/config.py` | [14_config.md](manual/14_config.md) | ✅ |
| 15 | `api/infrastructure/cache.py` | [15_cache.md](manual/15_cache.md) | ✅ |
| 16 | `api/infrastructure/google_classroom_client.py` | [16_google_client.md](manual/16_google_client.md) | ✅ |
| 17 | `api/infrastructure/mappers/__init__.py` | [17_mappers_init.md](manual/17_mappers_init.md) | ✅ |
| 18 | `api/infrastructure/mappers/classroom_mapper.py` | [18_classroom_mapper.md](manual/18_classroom_mapper.md) | ✅ |
| 19 | `api/infrastructure/repositories/google_classroom_repository.py` | [19_google_repository.md](manual/19_google_repository.md) | ✅ |

### 6. Application Layer

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 20 | `api/application/use_cases/list_user_courses.py` | [20_list_user_courses.md](manual/20_list_user_courses.md) | ✅ |
| 21 | `api/application/use_cases/list_course_materials.py` | [21_list_course_materials.md](manual/21_list_course_materials.md) | ✅ |

### 7. API Layer (Pendiente)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 22 | `api/routes/auth.py` | 22_auth_routes.md | ⏳ |
| 23 | `api/routes/courses.py` | 23_courses_routes.md | ⏳ |
| 24 | `api/routes/materials.py` | 24_materials_routes.md | ⏳ |

---

## 📊 Progreso

- **Archivos documentados**: 21/24
- **Progreso**: 87.5%
- **Pendiente**: API Layer (routes)

---

## 🎯 Estructura de Cada Manual

Cada manual técnico incluye:

1. **Propósito y Trazabilidad** — Qué hace y por qué existe
2. **Estrategia de Construcción Incremental** — Paso a paso
3. **Código Clave** — Fragmentos importantes con explicaciones
4. **🔥 Prueba de Fuego** — Comando exacto + salida esperada
5. **🔍 Análisis Dual** — Por qué SÍ / Por qué NO
6. **🎓 Conceptos Educativos** — Explicaciones de patrones

---

## 📖 Documentación Relacionada

- [01_planificacion_analisis.md](01_planificacion_analisis.md) — Planificación y requisitos
- [02_a_arquitectura_patrones.md](02_a_arquitectura_patrones.md) — Arquitectura Clean
- [02_b_modelado_datos.md](02_b_modelado_datos.md) — Modelo de datos
- [02_c_api_dinamica.md](02_c_api_dinamica.md) — API y endpoints
- [03_estrategia_datos.md](03_estrategia_datos.md) — Estrategia de datos

---

**Nota:** Siguiendo la numeración 01-21, puedes replicar todo el backend desde cero.
