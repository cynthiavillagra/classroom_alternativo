# 📚 Índice de Manuales Técnicos — Classroom Explorer

> **Versión**: 3.0  
> **Fecha**: 2025-12-14  
> **Estado**: ✅ Completo

---

## 📖 Orden de Construcción (Correcto)

**Filosofía:** Antes de escribir código, el entorno debe estar configurado.

```
1. requirements.txt      → Dependencias
2. .env.example          → Variables de entorno (placeholders)
3. setup_externo.md      → Cómo obtener credenciales
4. README.md             → Documentación del proyecto
5. vercel.json           → Configuración de deploy
... luego viene el código
```

---

## 📁 Secuencia Completa de Construcción

### 1. Configuración de Entorno (01-05)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 01 | `requirements.txt` | [01_requirements.md](manual/01_requirements.md) | ✅ |
| 02 | `.env.example` | [02_env_example.md](manual/02_env_example.md) | ✅ |
| 03 | `docs/setup_externo.md` | [03_setup_externo.md](manual/03_setup_externo.md) | ✅ |
| 04 | `README.md` | [04_readme.md](manual/04_readme.md) | ✅ |
| 05 | `vercel.json` | [05_vercel.md](manual/05_vercel.md) | ✅ |

### 2. Domain Layer - Entities (06-10)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 06 | `api/domain/entities/__init__.py` | [06_entities_init.md](manual/06_entities_init.md) | ✅ |
| 07 | `api/domain/entities/material_type.py` | [07_material_type.md](manual/07_material_type.md) | ✅ |
| 08 | `api/domain/entities/course_state.py` | [08_course_state.md](manual/08_course_state.md) | ✅ |
| 09 | `api/domain/entities/course.py` | [09_course.md](manual/09_course.md) | ✅ |
| 10 | `api/domain/entities/material.py` | [10_material.md](manual/10_material.md) | ✅ |

### 3. Domain Layer - Factories (11-13)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 11 | `api/domain/factories/__init__.py` | [11_factories_init.md](manual/11_factories_init.md) | ✅ |
| 12 | `api/domain/factories/course_factory.py` | [12_course_factory.md](manual/12_course_factory.md) | ✅ |
| 13 | `api/domain/factories/material_factory.py` | [13_material_factory.md](manual/13_material_factory.md) | ✅ |

### 4. Domain Layer - Interfaces (14-15)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 14 | `api/domain/interfaces/__init__.py` | [14_interfaces_init.md](manual/14_interfaces_init.md) | ✅ |
| 15 | `api/domain/interfaces/classroom_repository.py` | [15_classroom_repository.md](manual/15_classroom_repository.md) | ✅ |

### 5. Infrastructure Layer (16-21)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 16 | `api/infrastructure/config.py` | [16_config.md](manual/16_config.md) | ✅ |
| 17 | `api/infrastructure/cache.py` | [17_cache.md](manual/17_cache.md) | ✅ |
| 18 | `api/infrastructure/google_classroom_client.py` | [18_google_client.md](manual/18_google_client.md) | ✅ |
| 19 | `api/infrastructure/mappers/__init__.py` | [19_mappers_init.md](manual/19_mappers_init.md) | ✅ |
| 20 | `api/infrastructure/mappers/classroom_mapper.py` | [20_classroom_mapper.md](manual/20_classroom_mapper.md) | ✅ |
| 21 | `api/infrastructure/repositories/google_classroom_repository.py` | [21_google_repository.md](manual/21_google_repository.md) | ✅ |

### 6. Application Layer (22-23)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 22 | `api/application/use_cases/list_user_courses.py` | [22_list_user_courses.md](manual/22_list_user_courses.md) | ✅ |
| 23 | `api/application/use_cases/list_course_materials.py` | [23_list_course_materials.md](manual/23_list_course_materials.md) | ✅ |

### 7. API Layer (24-27)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 24 | `api/routes/auth.py` | [24_auth_routes.md](manual/24_auth_routes.md) | ✅ |
| 25 | `api/routes/courses.py` | [25_courses_routes.md](manual/25_courses_routes.md) | ✅ |
| 26 | `api/routes/materials.py` | [26_materials_routes.md](manual/26_materials_routes.md) | ✅ |
| 27 | `main.py` | [27_main_server.md](manual/27_main_server.md) | ✅ |

### 8. Frontend Layer (28)

| # | Archivo | Manual | Estado |
|---|---------|--------|--------|
| 28 | `public/materials.html` | [28_materials_frontend.md](manual/28_materials_frontend.md) | ✅ |

---

## 📊 Resumen

- **Total de manuales**: 28
- **Orden correcto**: Configuración → Domain → Infrastructure → Application → API → Frontend
- **Filosofía**: Entorno configurado ANTES de código

---

## 🆕 Changelog

| Versión | Fecha | Cambio |
|---------|-------|--------|
| 3.0 | 2025-12-14 | Índice inicial con 27 manuales |
| 3.1 | 2025-12-20 | Agregado manual #28: Frontend materials.html |

---

## 🤖 AI Stack

Generado mediante metodología SDLC V5 usando Google Antigravity + Claude Opus 4.5
