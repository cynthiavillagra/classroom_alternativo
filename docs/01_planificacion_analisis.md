# 📋 Planificación y Análisis — Classroom Explorer

> **Versión**: 1.0  
> **Fecha**: 2025-12-14  
> **Autor**: Equipo de Desarrollo  
> **Estado**: 📝 En Revisión

---

## 📑 Índice

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Plan de Trabajo (Sprints)](#2-plan-de-trabajo-sprints)
3. [Definición de Requisitos](#3-definición-de-requisitos)
4. [Análisis Funcional Detallado](#4-análisis-funcional-detallado)
5. [Modularización](#5-modularización)
6. [Análisis de Riesgos](#6-análisis-de-riesgos)

---

## 1. Resumen Ejecutivo

### 1.1 Definición del Proyecto

**Classroom Explorer** es una Web Application que actúa como un explorador avanzado de materiales de Google Classroom. A diferencia de la interfaz nativa de Classroom, esta aplicación proporciona una vista unificada de todos los materiales con capacidades avanzadas de filtrado y organización.

### 1.2 Objetivo Principal

Desarrollar una aplicación web que permita a los usuarios visualizar, filtrar y acceder rápidamente a los materiales de sus cursos de Google Classroom, mejorando significativamente la experiencia de navegación respecto a la interfaz nativa.

**Objetivos Secundarios (Educativos):**
- Aprender a programar siguiendo principios de Arquitectura Limpia (Clean Architecture)
- Aplicar Programación Orientada a Objetos (POO) de manera profesional
- Implementar trazabilidad completa desde requisitos hasta código
- Practicar metodologías de desarrollo profesional (SDLC)

### 1.3 Alcance

#### ✅ Dentro del Alcance (IN)

| ID | Funcionalidad |
|----|---------------|
| IN-01 | Autenticación mediante Google OAuth 2.0 |
| IN-02 | Listado de cursos del usuario autenticado |
| IN-03 | Listado de materiales por curso |
| IN-04 | Vista de lista (detalle) de materiales |
| IN-05 | Vista de tarjetas (cards) de materiales |
| IN-06 | Filtrado por tipo de archivo |
| IN-07 | Filtrado por curso/materia |
| IN-08 | Filtrado por rango de fechas |
| IN-09 | Enlace directo al material en Classroom/Drive |
| IN-10 | Interfaz responsive (mobile/desktop) |

#### ❌ Fuera del Alcance (OUT)

| ID | Funcionalidad | Justificación |
|----|---------------|---------------|
| OUT-01 | Almacenamiento local de materiales | Complejidad + Almacenamiento |
| OUT-02 | Edición de materiales | Fuera del objetivo (solo lectura) |
| OUT-03 | Sistema de notificaciones | Fase futura |
| OUT-04 | Favoritos/Marcadores persistentes | Requiere base de datos |
| OUT-05 | Búsqueda por contenido del archivo | Requiere indexación |

### 1.4 Stack Tecnológico

| Capa | Tecnología | Justificación |
|------|------------|---------------|
| **Frontend** | HTML5 + CSS3 + JavaScript Vanilla | Simplicidad, sin dependencias, máximo control |
| **Backend** | Python 3.11+ con POO | Claridad sintáctica, ideal para aprendizaje |
| **API Gateway** | Vercel Serverless Functions | Sin servidor, escalable, gratuito |
| **Autenticación** | Google OAuth 2.0 | Estándar de la industria |
| **Fuente de Datos** | Google Classroom API | Acceso directo a los materiales |

---

## 2. Plan de Trabajo (Sprints)

### 2.1 Metodología

Usaremos **Sprints de 1 semana** con entregas incrementales. Cada sprint tiene un objetivo claro y entregables verificables.

### 2.2 Roadmap de Sprints

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FASE DE PLANIFICACIÓN                         │
├─────────────────────────────────────────────────────────────────────────┤
│ Sprint 0 │ Documentación y Setup                                        │
│          │ • Planificación y análisis (este documento)                  │
│          │ • Arquitectura y diseño técnico                              │
│          │ • Setup del repositorio y entorno local                      │
└──────────┴──────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           FASE DE DESARROLLO                            │
├─────────────────────────────────────────────────────────────────────────┤
│ Sprint 1 │ Domain Layer (Fundamentos)                                   │
│          │ • Entidades: Course, Material, MaterialType                  │
│          │ • Value Objects y validaciones                               │
│          │ • Tests unitarios del dominio                                │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Sprint 2 │ Infrastructure Layer (Google API)                            │
│          │ • Cliente HTTP para Google Classroom API                     │
│          │ • Mappers: API Response → Domain Entities                    │
│          │ • Manejo de errores y reintentos                             │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Sprint 3 │ Application Layer (Casos de Uso)                             │
│          │ • UC: ListUserCourses                                        │
│          │ • UC: ListCourseMaterials                                    │
│          │ • UC: FilterMaterials                                        │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Sprint 4 │ API Layer (Endpoints REST)                                   │
│          │ • Endpoint: GET /api/courses                                 │
│          │ • Endpoint: GET /api/courses/{id}/materials                  │
│          │ • Middleware de autenticación                                │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Sprint 5 │ Frontend - Estructura Base                                   │
│          │ • HTML semántico y accesible                                 │
│          │ • Sistema de diseño (CSS custom properties)                  │
│          │ • JavaScript: Módulos y conexión API                         │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Sprint 6 │ Frontend - Vistas y Filtros                                  │
│          │ • Componente: Vista Lista                                    │
│          │ • Componente: Vista Cards                                    │
│          │ • Componente: Panel de Filtros                               │
│          │ • Toggle entre vistas                                        │
├──────────┼──────────────────────────────────────────────────────────────┤
│ Sprint 7 │ Autenticación Completa                                       │
│          │ • Flujo OAuth 2.0 completo                                   │
│          │ • Pantalla de login                                          │
│          │ • Manejo de sesión (tokens)                                  │
│          │ • Logout y refresh tokens                                    │
└──────────┴──────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           FASE DE DESPLIEGUE                            │
├─────────────────────────────────────────────────────────────────────────┤
│ Sprint 8 │ Testing, Deploy y Documentación                              │
│          │ • Tests de integración                                       │
│          │ • Deploy a Vercel (producción)                               │
│          │ • Manual de replicación final                                │
│          │ • Documentación de usuario                                   │
└──────────┴──────────────────────────────────────────────────────────────┘
```

### 2.3 Detalle por Sprint

| Sprint | Duración | Entregables | Criterio de Éxito |
|--------|----------|-------------|-------------------|
| **0** | 1 semana | Documentación completa | Documentos aprobados |
| **1** | 1 semana | Domain Layer + Tests | 100% tests pasando |
| **2** | 1 semana | Google API Client | Conexión exitosa local |
| **3** | 1 semana | Casos de Uso | Tests de integración OK |
| **4** | 1 semana | API REST funcional | Endpoints respondiendo |
| **5** | 1 semana | Frontend base | Renderiza datos mock |
| **6** | 1 semana | UI completa | Filtros funcionando |
| **7** | 1 semana | Auth completa | Login/logout funcional |
| **8** | 1 semana | App desplegada | URL pública activa |

---

## 3. Definición de Requisitos

### 3.1 Requisitos Funcionales (MoSCoW)

#### 🔴 Must Have (Obligatorios)

| ID | Requisito | Descripción | Sprint |
|----|-----------|-------------|--------|
| RF-M01 | Login con Google | El usuario debe poder autenticarse con su cuenta de Google/Classroom | S7 |
| RF-M02 | Listar Cursos | El sistema debe mostrar todos los cursos del usuario autenticado | S3-S4 |
| RF-M03 | Listar Materiales | El sistema debe mostrar los materiales de un curso seleccionado | S3-S4 |
| RF-M04 | Abrir Material | Al hacer clic, el material debe abrirse en una nueva pestaña (Classroom/Drive) | S5 |
| RF-M05 | Vista Lista | Los materiales deben poder verse en formato lista con detalles | S6 |
| RF-M06 | Vista Cards | Los materiales deben poder verse en formato tarjetas visuales | S6 |
| RF-M07 | Filtrar por Curso | El usuario debe poder filtrar materiales por curso/materia | S6 |
| RF-M08 | Logout | El usuario debe poder cerrar sesión de forma segura | S7 |

#### 🟡 Should Have (Importantes)

| ID | Requisito | Descripción | Sprint |
|----|-----------|-------------|--------|
| RF-S01 | Filtrar por Tipo | Filtrar materiales por tipo (PDF, Video, Doc, Link, etc.) | S6 |
| RF-S02 | Filtrar por Fecha | Filtrar materiales por rango de fechas | S6 |
| RF-S03 | Ordenar Materiales | Ordenar por nombre, fecha o tipo | S6 |
| RF-S04 | Contador de Resultados | Mostrar cantidad de materiales encontrados | S6 |
| RF-S05 | Estado de Carga | Indicadores visuales durante la carga de datos | S5 |

#### 🟢 Could Have (Deseables)

| ID | Requisito | Descripción | Sprint |
|----|-----------|-------------|--------|
| RF-C01 | Búsqueda por Nombre | Buscar materiales por nombre/título | Futuro |
| RF-C02 | Vista Previa | Mostrar preview del material (si es imagen/PDF) | Futuro |
| RF-C03 | Modo Oscuro | Alternar entre tema claro y oscuro | Futuro |
| RF-C04 | Recordar Preferencias | Guardar última vista y filtros usados (localStorage) | Futuro |

#### ⚪ Won't Have (Excluidos - Esta Versión)

| ID | Requisito | Justificación |
|----|-----------|---------------|
| RF-W01 | Descargar Materiales | Complejidad + Permisos de Drive |
| RF-W02 | Editar Materiales | Fuera del alcance (solo lectura) |
| RF-W03 | Sistema de Favoritos | Requiere persistencia propia |
| RF-W04 | Notificaciones Push | Complejidad excesiva para MVP |

### 3.2 Requisitos No Funcionales

#### 🔐 Seguridad (RNF-SEC)

| ID | Requisito | Métrica | Prioridad |
|----|-----------|---------|-----------|
| RNF-SEC01 | Zero-Trust en Código | 0 credenciales hardcodeadas | CRÍTICO |
| RNF-SEC02 | OAuth 2.0 Estándar | Cumplimiento RFC 6749 | CRÍTICO |
| RNF-SEC03 | HTTPS Obligatorio | 100% tráfico cifrado | CRÍTICO |
| RNF-SEC04 | Tokens Seguros | Almacenamiento seguro, no localStorage | ALTO |
| RNF-SEC05 | CORS Configurado | Solo orígenes permitidos | ALTO |

#### ⚡ Rendimiento (RNF-PERF)

| ID | Requisito | Métrica | Prioridad |
|----|-----------|---------|-----------|
| RNF-PERF01 | Tiempo de Carga Inicial | < 3 segundos | ALTO |
| RNF-PERF02 | Respuesta de API | < 500ms (p95) | MEDIO |
| RNF-PERF03 | Cambio de Vista | < 100ms | MEDIO |
| RNF-PERF04 | Filtrado Local | < 50ms | MEDIO |

#### 🎨 Usabilidad (RNF-UX)

| ID | Requisito | Métrica | Prioridad |
|----|-----------|---------|-----------|
| RNF-UX01 | Responsive Design | Funcional en 320px - 1920px | ALTO |
| RNF-UX02 | Accesibilidad Básica | Navegable por teclado | MEDIO |
| RNF-UX03 | Feedback Visual | Estados: loading, error, vacío | ALTO |
| RNF-UX04 | Consistencia Visual | Sistema de diseño unificado | MEDIO |

#### 🏗️ Mantenibilidad (RNF-MANT)

| ID | Requisito | Métrica | Prioridad |
|----|-----------|---------|-----------|
| RNF-MANT01 | Arquitectura Limpia | Separación de capas estricta | CRÍTICO |
| RNF-MANT02 | Código Documentado | Docstrings en todas las clases | ALTO |
| RNF-MANT03 | Tests Unitarios | > 80% cobertura en Domain | ALTO |
| RNF-MANT04 | Convenciones de Código | PEP 8 (Python), ESLint (JS) | MEDIO |

---

## 4. Análisis Funcional Detallado

### 4.1 Historias de Usuario

#### HU-001: Autenticación con Google

```
COMO usuario de Google Classroom
QUIERO iniciar sesión con mi cuenta de Google
PARA acceder a mis materiales de forma segura

─────────────────────────────────────────────
CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────
✓ AC-001.1: Dado que estoy en la página de login,
            Cuando hago clic en "Iniciar con Google",
            Entonces se abre el flujo de autenticación de Google.

✓ AC-001.2: Dado que he autorizado la aplicación en Google,
            Cuando se completa el flujo OAuth,
            Entonces soy redirigido a la página principal con mi sesión activa.

✓ AC-001.3: Dado que la autenticación falla,
            Cuando Google rechaza el acceso,
            Entonces veo un mensaje de error descriptivo.

✓ AC-001.4: Dado que estoy autenticado,
            Cuando recargo la página,
            Entonces mi sesión persiste (dentro del tiempo de expiración).

─────────────────────────────────────────────
TRAZABILIDAD: RF-M01, RNF-SEC01, RNF-SEC02
─────────────────────────────────────────────
```

#### HU-002: Visualización de Cursos

```
COMO usuario autenticado
QUIERO ver la lista de mis cursos de Classroom
PARA seleccionar de cuál quiero ver los materiales

─────────────────────────────────────────────
CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────
✓ AC-002.1: Dado que estoy autenticado,
            Cuando cargo la página principal,
            Entonces veo todos mis cursos activos de Classroom.

✓ AC-002.2: Dado que tengo cursos,
            Cuando veo la lista,
            Entonces cada curso muestra: nombre, sección (si existe), y estado.

✓ AC-002.3: Dado que no tengo cursos,
            Cuando cargo la página,
            Entonces veo un mensaje "No tienes cursos en Classroom".

✓ AC-002.4: Dado que ocurre un error de API,
            Cuando falla la carga,
            Entonces veo un mensaje de error con opción de reintentar.

─────────────────────────────────────────────
TRAZABILIDAD: RF-M02, RNF-UX03
─────────────────────────────────────────────
```

#### HU-003: Visualización de Materiales

```
COMO usuario autenticado
QUIERO ver los materiales de un curso seleccionado
PARA encontrar el recurso que necesito

─────────────────────────────────────────────
CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────
✓ AC-003.1: Dado que selecciono un curso,
            Cuando se cargan los materiales,
            Entonces veo todos los materiales asociados a ese curso.

✓ AC-003.2: Dado que hay materiales,
            Cuando veo la lista,
            Entonces cada material muestra: título, tipo, fecha de creación.

✓ AC-003.3: Dado que un curso no tiene materiales,
            Cuando lo selecciono,
            Entonces veo un mensaje "Este curso no tiene materiales".

✓ AC-003.4: Dado que hay materiales cargando,
            Cuando espero,
            Entonces veo un indicador de carga (spinner/skeleton).

─────────────────────────────────────────────
TRAZABILIDAD: RF-M03, RNF-UX03, RNF-PERF01
─────────────────────────────────────────────
```

#### HU-004: Acceso Directo a Materiales

```
COMO usuario
QUIERO hacer clic en un material
PARA abrirlo directamente en Classroom o Drive

─────────────────────────────────────────────
CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────
✓ AC-004.1: Dado que hago clic en un material,
            Cuando se procesa el clic,
            Entonces se abre una nueva pestaña con el recurso original.

✓ AC-004.2: Dado que el material es de Drive,
            Cuando hago clic,
            Entonces se abre la vista de Drive del archivo.

✓ AC-004.3: Dado que el material es un link externo,
            Cuando hago clic,
            Entonces se abre el link en nueva pestaña.

─────────────────────────────────────────────
TRAZABILIDAD: RF-M04
─────────────────────────────────────────────
```

#### HU-005: Cambio de Vista (Lista/Cards)

```
COMO usuario
QUIERO alternar entre vista de lista y vista de tarjetas
PARA ver los materiales en el formato que prefiera

─────────────────────────────────────────────
CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────
✓ AC-005.1: Dado que estoy viendo materiales,
            Cuando hago clic en el botón de vista lista,
            Entonces los materiales se muestran en formato tabla/lista.

✓ AC-005.2: Dado que estoy viendo materiales,
            Cuando hago clic en el botón de vista cards,
            Entonces los materiales se muestran en formato tarjetas.

✓ AC-005.3: Dado que cambio de vista,
            Cuando se renderiza la nueva vista,
            Entonces la transición es suave (< 100ms).

✓ AC-005.4: Dado que tengo filtros activos,
            Cuando cambio de vista,
            Entonces los filtros se mantienen aplicados.

─────────────────────────────────────────────
TRAZABILIDAD: RF-M05, RF-M06, RNF-PERF03
─────────────────────────────────────────────
```

#### HU-006: Filtrado de Materiales

```
COMO usuario
QUIERO filtrar materiales por diferentes criterios
PARA encontrar rápidamente lo que busco

─────────────────────────────────────────────
CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────
✓ AC-006.1: Dado que selecciono un filtro de curso,
            Cuando aplico el filtro,
            Entonces solo veo materiales de ese curso.

✓ AC-006.2: Dado que selecciono un filtro de tipo (PDF, Video, etc.),
            Cuando aplico el filtro,
            Entonces solo veo materiales de ese tipo.

✓ AC-006.3: Dado que selecciono un rango de fechas,
            Cuando aplico el filtro,
            Entonces solo veo materiales creados en ese rango.

✓ AC-006.4: Dado que combino múltiples filtros,
            Cuando aplico los filtros,
            Entonces veo materiales que cumplen TODOS los criterios (AND).

✓ AC-006.5: Dado que aplico filtros,
            Cuando veo los resultados,
            Entonces veo un contador con la cantidad de materiales encontrados.

✓ AC-006.6: Dado que quiero limpiar filtros,
            Cuando hago clic en "Limpiar filtros",
            Entonces se muestran todos los materiales nuevamente.

─────────────────────────────────────────────
TRAZABILIDAD: RF-M07, RF-S01, RF-S02, RF-S04, RNF-PERF04
─────────────────────────────────────────────
```

#### HU-007: Cierre de Sesión

```
COMO usuario autenticado
QUIERO cerrar mi sesión
PARA proteger mi información en dispositivos compartidos

─────────────────────────────────────────────
CRITERIOS DE ACEPTACIÓN:
─────────────────────────────────────────────
✓ AC-007.1: Dado que estoy autenticado,
            Cuando hago clic en "Cerrar Sesión",
            Entonces mi sesión se invalida.

✓ AC-007.2: Dado que cerré sesión,
            Cuando intento acceder a la app,
            Entonces soy redirigido al login.

✓ AC-007.3: Dado que cerré sesión,
            Cuando reviso el almacenamiento local,
            Entonces no quedan tokens ni datos de sesión.

─────────────────────────────────────────────
TRAZABILIDAD: RF-M08, RNF-SEC04
─────────────────────────────────────────────
```

---

### 4.2 Casos de Uso (Formato Estricto)

#### CU-001: Iniciar Sesión con Google

```
╔══════════════════════════════════════════════════════════════════╗
║  CASO DE USO: CU-001 — Iniciar Sesión con Google                 ║
╠══════════════════════════════════════════════════════════════════╣
║  ACTOR PRINCIPAL: Usuario (Profesor/Estudiante)                  ║
║  ACTORES SECUNDARIOS: Google OAuth Service, Google Classroom API ║
║  PRECONDICIONES:                                                 ║
║    • El usuario tiene una cuenta de Google con acceso a Classroom║
║    • El usuario no está autenticado en la aplicación             ║
║  POSTCONDICIONES:                                                ║
║    • El usuario tiene una sesión activa                          ║
║    • Los tokens de acceso están almacenados de forma segura      ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJO PRINCIPAL:                                                ║
╠══════════════════════════════════════════════════════════════════╣
║  1. El usuario accede a la página de login                       ║
║  2. El usuario hace clic en "Iniciar con Google"                 ║
║  3. El sistema redirige a Google OAuth (consent screen)          ║
║  4. El usuario selecciona su cuenta de Google                    ║
║  5. El usuario autoriza los permisos solicitados                 ║
║  6. Google redirige al callback con código de autorización       ║
║  7. El sistema intercambia el código por access_token            ║
║  8. El sistema valida el token con Google                        ║
║  9. El sistema crea la sesión del usuario                        ║
║  10. El sistema redirige a la página principal                   ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJOS ALTERNATIVOS:                                            ║
╠══════════════════════════════════════════════════════════════════╣
║  4a. El usuario cancela el login en Google:                      ║
║      4a.1. Google redirige al callback con error                 ║
║      4a.2. El sistema muestra "Autenticación cancelada"          ║
║      4a.3. El sistema permanece en la página de login            ║
║                                                                  ║
║  5a. El usuario deniega permisos:                                ║
║      5a.1. El sistema muestra mensaje explicando permisos        ║
║      5a.2. El sistema ofrece reintentar                          ║
║                                                                  ║
║  7a. El código de autorización es inválido o expiró:             ║
║      7a.1. El sistema muestra "Sesión expirada, intente de nuevo"║
║      7a.2. El sistema redirige a la página de login              ║
╠══════════════════════════════════════════════════════════════════╣
║  EXCEPCIONES:                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  E1. Error de red durante OAuth:                                 ║
║      • Mostrar: "Error de conexión. Verifique su internet."      ║
║                                                                  ║
║  E2. Google API no disponible:                                   ║
║      • Mostrar: "Servicio temporalmente no disponible."          ║
║      • Registrar error en logs                                   ║
║                                                                  ║
║  E3. Usuario sin acceso a Classroom:                             ║
║      • Mostrar: "Su cuenta no tiene acceso a Google Classroom."  ║
╚══════════════════════════════════════════════════════════════════╝
```

#### CU-002: Listar Cursos del Usuario

```
╔══════════════════════════════════════════════════════════════════╗
║  CASO DE USO: CU-002 — Listar Cursos del Usuario                 ║
╠══════════════════════════════════════════════════════════════════╣
║  ACTOR PRINCIPAL: Usuario Autenticado                            ║
║  ACTORES SECUNDARIOS: Google Classroom API                       ║
║  PRECONDICIONES:                                                 ║
║    • El usuario está autenticado                                 ║
║    • El token de acceso es válido                                ║
║  POSTCONDICIONES:                                                ║
║    • Se muestra la lista de cursos del usuario                   ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJO PRINCIPAL:                                                ║
╠══════════════════════════════════════════════════════════════════╣
║  1. El usuario accede a la página principal                      ║
║  2. El sistema muestra indicador de carga                        ║
║  3. El sistema solicita cursos a Google Classroom API            ║
║  4. La API responde con lista de cursos                          ║
║  5. El sistema transforma la respuesta a entidades de dominio    ║
║  6. El sistema renderiza la lista de cursos                      ║
║  7. El usuario ve sus cursos con nombre, sección y estado        ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJOS ALTERNATIVOS:                                            ║
╠══════════════════════════════════════════════════════════════════╣
║  4a. El usuario no tiene cursos:                                 ║
║      4a.1. El sistema muestra estado vacío                       ║
║      4a.2. Mensaje: "No tienes cursos en Classroom"              ║
║                                                                  ║
║  3a. Token expirado:                                             ║
║      3a.1. El sistema intenta refresh del token                  ║
║      3a.2. Si falla, redirige a login                            ║
╠══════════════════════════════════════════════════════════════════╣
║  EXCEPCIONES:                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  E1. Error de API (500):                                         ║
║      • Mostrar: "Error al cargar cursos. Intente nuevamente."    ║
║      • Botón: "Reintentar"                                       ║
║                                                                  ║
║  E2. Rate limit excedido (429):                                  ║
║      • Mostrar: "Demasiadas solicitudes. Espere un momento."     ║
║      • Retry automático con backoff exponencial                  ║
╚══════════════════════════════════════════════════════════════════╝
```

#### CU-003: Listar Materiales de un Curso

```
╔══════════════════════════════════════════════════════════════════╗
║  CASO DE USO: CU-003 — Listar Materiales de un Curso             ║
╠══════════════════════════════════════════════════════════════════╣
║  ACTOR PRINCIPAL: Usuario Autenticado                            ║
║  ACTORES SECUNDARIOS: Google Classroom API                       ║
║  PRECONDICIONES:                                                 ║
║    • El usuario está autenticado                                 ║
║    • Se ha seleccionado un curso                                 ║
║  POSTCONDICIONES:                                                ║
║    • Se muestran los materiales del curso seleccionado           ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJO PRINCIPAL:                                                ║
╠══════════════════════════════════════════════════════════════════╣
║  1. El usuario selecciona un curso                               ║
║  2. El sistema muestra indicador de carga                        ║
║  3. El sistema solicita courseWork y courseWorkMaterials         ║
║  4. La API responde con los materiales                           ║
║  5. El sistema transforma respuestas a entidades Material        ║
║  6. El sistema agrupa y ordena los materiales                    ║
║  7. El sistema renderiza en la vista activa (lista o cards)      ║
║  8. El usuario ve los materiales con título, tipo y fecha        ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJOS ALTERNATIVOS:                                            ║
╠══════════════════════════════════════════════════════════════════╣
║  4a. El curso no tiene materiales:                               ║
║      4a.1. El sistema muestra estado vacío                       ║
║      4a.2. Mensaje: "Este curso no tiene materiales"             ║
║                                                                  ║
║  7a. Usuario prefiere otra vista:                                ║
║      7a.1. Usuario hace clic en toggle de vista                  ║
║      7a.2. Sistema re-renderiza con nueva vista                  ║
╠══════════════════════════════════════════════════════════════════╣
║  EXCEPCIONES:                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  E1. Curso no encontrado (404):                                  ║
║      • Mostrar: "El curso ya no existe o no tienes acceso."      ║
║      • Redirigir a lista de cursos                               ║
║                                                                  ║
║  E2. Permisos insuficientes (403):                               ║
║      • Mostrar: "No tienes permiso para ver este curso."         ║
╚══════════════════════════════════════════════════════════════════╝
```

#### CU-004: Filtrar Materiales

```
╔══════════════════════════════════════════════════════════════════╗
║  CASO DE USO: CU-004 — Filtrar Materiales                        ║
╠══════════════════════════════════════════════════════════════════╣
║  ACTOR PRINCIPAL: Usuario Autenticado                            ║
║  ACTORES SECUNDARIOS: Ninguno (operación local)                  ║
║  PRECONDICIONES:                                                 ║
║    • Hay materiales cargados en la vista                         ║
║  POSTCONDICIONES:                                                ║
║    • Solo se muestran materiales que cumplen los filtros         ║
║    • El contador de resultados se actualiza                      ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJO PRINCIPAL:                                                ║
╠══════════════════════════════════════════════════════════════════╣
║  1. El usuario abre el panel de filtros                          ║
║  2. El usuario selecciona criterios de filtrado:                 ║
║     - Curso (dropdown)                                           ║
║     - Tipo de archivo (checkboxes)                               ║
║     - Rango de fechas (date pickers)                             ║
║  3. El sistema aplica los filtros en tiempo real                 ║
║  4. El sistema actualiza la vista con resultados filtrados       ║
║  5. El sistema muestra contador: "X materiales encontrados"      ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJOS ALTERNATIVOS:                                            ║
╠══════════════════════════════════════════════════════════════════╣
║  4a. Ningún material cumple los filtros:                         ║
║      4a.1. El sistema muestra estado vacío                       ║
║      4a.2. Mensaje: "No hay materiales con estos filtros"        ║
║      4a.3. Sugerencia: "Prueba con otros criterios"              ║
║                                                                  ║
║  2a. Usuario quiere limpiar filtros:                             ║
║      2a.1. Usuario hace clic en "Limpiar filtros"                ║
║      2a.2. Sistema resetea todos los filtros                     ║
║      2a.3. Sistema muestra todos los materiales                  ║
╠══════════════════════════════════════════════════════════════════╣
║  EXCEPCIONES:                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  E1. Fecha inválida:                                             ║
║      • El date picker previene fechas inválidas                  ║
║      • Si fecha_desde > fecha_hasta, intercambiar                ║
╚══════════════════════════════════════════════════════════════════╝
```

#### CU-005: Abrir Material Externo

```
╔══════════════════════════════════════════════════════════════════╗
║  CASO DE USO: CU-005 — Abrir Material Externo                    ║
╠══════════════════════════════════════════════════════════════════╣
║  ACTOR PRINCIPAL: Usuario Autenticado                            ║
║  ACTORES SECUNDARIOS: Google Drive, Google Classroom, Web Externa║
║  PRECONDICIONES:                                                 ║
║    • Hay materiales visibles en la interfaz                      ║
║  POSTCONDICIONES:                                                ║
║    • Se abre una nueva pestaña con el recurso                    ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJO PRINCIPAL:                                                ║
╠══════════════════════════════════════════════════════════════════╣
║  1. El usuario identifica el material deseado                    ║
║  2. El usuario hace clic en el material (o botón "Abrir")        ║
║  3. El sistema determina el tipo de enlace:                      ║
║     - driveFile: Abre en Google Drive                            ║
║     - youtubeVideo: Abre en YouTube                              ║
║     - link: Abre la URL externa                                  ║
║     - form: Abre Google Forms                                    ║
║  4. El sistema abre nueva pestaña con target="_blank"            ║
║  5. El usuario interactúa con el recurso en la nueva pestaña     ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJOS ALTERNATIVOS:                                            ║
╠══════════════════════════════════════════════════════════════════╣
║  Ninguno                                                         ║
╠══════════════════════════════════════════════════════════════════╣
║  EXCEPCIONES:                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  E1. Popup bloqueado:                                            ║
║      • Mostrar tooltip: "Permite popups para abrir materiales"   ║
║                                                                  ║
║  E2. Enlace roto/inválido:                                       ║
║      • La pestaña nueva mostrará error de Google/Drive           ║
║      • (No controlable desde nuestra app)                        ║
╚══════════════════════════════════════════════════════════════════╝
```

#### CU-006: Cerrar Sesión

```
╔══════════════════════════════════════════════════════════════════╗
║  CASO DE USO: CU-006 — Cerrar Sesión                             ║
╠══════════════════════════════════════════════════════════════════╣
║  ACTOR PRINCIPAL: Usuario Autenticado                            ║
║  ACTORES SECUNDARIOS: Ninguno                                    ║
║  PRECONDICIONES:                                                 ║
║    • El usuario tiene una sesión activa                          ║
║  POSTCONDICIONES:                                                ║
║    • La sesión es invalidada                                     ║
║    • Todos los tokens son eliminados                             ║
║    • El usuario es redirigido al login                           ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJO PRINCIPAL:                                                ║
╠══════════════════════════════════════════════════════════════════╣
║  1. El usuario hace clic en "Cerrar Sesión" (menú de usuario)    ║
║  2. El sistema revoca el token en Google (opcional)              ║
║  3. El sistema elimina tokens del almacenamiento                 ║
║  4. El sistema limpia cualquier caché local                      ║
║  5. El sistema redirige a la página de login                     ║
║  6. El sistema muestra confirmación: "Sesión cerrada"            ║
╠══════════════════════════════════════════════════════════════════╣
║  FLUJOS ALTERNATIVOS:                                            ║
╠══════════════════════════════════════════════════════════════════╣
║  2a. Error al revocar token en Google:                           ║
║      2a.1. El sistema ignora el error (no crítico)               ║
║      2a.2. Continúa con pasos 3-6                                ║
║      2a.3. El token expirará naturalmente                        ║
╠══════════════════════════════════════════════════════════════════╣
║  EXCEPCIONES:                                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  Ninguna (operación debe completarse siempre)                    ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 5. Modularización

### 5.1 Arquitectura por Capas

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MÓDULOS DEL SISTEMA                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    📱 MÓDULO: PRESENTACIÓN                    │  │
│  │  (Frontend: HTML/CSS/JS)                                      │  │
│  │                                                               │  │
│  │  • Componentes UI (Lista, Cards, Filtros, Header)             │  │
│  │  • Manejo de eventos                                          │  │
│  │  • Renderizado de vistas                                      │  │
│  │  • Llamadas HTTP al backend                                   │  │
│  │                                                               │  │
│  │  Requisitos: RF-M05, RF-M06, RF-S05, RNF-UX01-04              │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    🔌 MÓDULO: API                             │  │
│  │  (Backend: Python - Vercel Functions)                         │  │
│  │                                                               │  │
│  │  • Endpoints REST                                             │  │
│  │  • Validación de requests                                     │  │
│  │  • Serialización de responses                                 │  │
│  │  • Middleware de autenticación                                │  │
│  │                                                               │  │
│  │  Requisitos: RF-M02, RF-M03, RNF-SEC05, RNF-PERF02            │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    ⚙️ MÓDULO: APLICACIÓN                      │  │
│  │  (Casos de Uso)                                               │  │
│  │                                                               │  │
│  │  • ListUserCoursesUseCase                                     │  │
│  │  • ListCourseMaterialsUseCase                                 │  │
│  │  • FilterMaterialsUseCase                                     │  │
│  │                                                               │  │
│  │  Requisitos: RF-M02, RF-M03, RF-M07, RF-S01, RF-S02           │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    🏛️ MÓDULO: DOMINIO                         │  │
│  │  (Entidades de Negocio - POO Pura)                            │  │
│  │                                                               │  │
│  │  • Course (id, name, section, state)                          │  │
│  │  • Material (id, title, type, url, createdAt, courseId)       │  │
│  │  • MaterialType (enum: PDF, VIDEO, DOC, LINK, FORM, etc.)     │  │
│  │                                                               │  │
│  │  Requisitos: RNF-MANT01, RNF-MANT02, RNF-MANT03               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    🔧 MÓDULO: INFRAESTRUCTURA                 │  │
│  │  (Adaptadores Externos)                                       │  │
│  │                                                               │  │
│  │  • GoogleClassroomClient (HTTP requests a Google API)         │  │
│  │  • GoogleOAuthClient (Manejo de tokens)                       │  │
│  │  • ResponseMappers (API → Entidades)                          │  │
│  │                                                               │  │
│  │  Requisitos: RF-M01, RF-M08, RNF-SEC01-04                     │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    🔐 MÓDULO: AUTENTICACIÓN                   │  │
│  │  (OAuth 2.0)                                                  │  │
│  │                                                               │  │
│  │  • Flujo OAuth 2.0 completo                                   │  │
│  │  • Manejo de tokens (access, refresh)                         │  │
│  │  • Sesión de usuario                                          │  │
│  │  • Logout y revocación                                        │  │
│  │                                                               │  │
│  │  Requisitos: RF-M01, RF-M08, RNF-SEC01-04                     │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Estructura de Carpetas Propuesta

```
classroom-explorer/
├── 📁 api/                          # Backend (Vercel Serverless)
│   ├── 📁 domain/                   # Capa de Dominio
│   │   ├── entities/
│   │   │   ├── course.py
│   │   │   ├── material.py
│   │   │   └── material_type.py
│   │   └── interfaces/
│   │       └── classroom_repository.py
│   │
│   ├── 📁 application/              # Capa de Aplicación
│   │   └── use_cases/
│   │       ├── list_courses.py
│   │       ├── list_materials.py
│   │       └── filter_materials.py
│   │
│   ├── 📁 infrastructure/           # Capa de Infraestructura
│   │   ├── google_classroom_client.py
│   │   ├── google_oauth_client.py
│   │   └── mappers/
│   │       └── classroom_mapper.py
│   │
│   ├── 📁 routes/                   # Endpoints API
│   │   ├── courses.py
│   │   ├── materials.py
│   │   └── auth.py
│   │
│   └── requirements.txt
│
├── 📁 public/                       # Frontend (Estático)
│   ├── index.html
│   ├── login.html
│   ├── 📁 css/
│   │   ├── variables.css            # Design tokens
│   │   ├── base.css                 # Reset y estilos base
│   │   ├── components.css           # Componentes reutilizables
│   │   └── pages.css                # Estilos específicos por página
│   │
│   ├── 📁 js/
│   │   ├── app.js                   # Entrada principal
│   │   ├── api.js                   # Cliente HTTP
│   │   ├── auth.js                  # Manejo de autenticación
│   │   ├── 📁 components/
│   │   │   ├── course-list.js
│   │   │   ├── material-list.js
│   │   │   ├── material-card.js
│   │   │   └── filter-panel.js
│   │   └── 📁 utils/
│   │       ├── date-formatter.js
│   │       └── material-icons.js
│   │
│   └── 📁 assets/
│       └── icons/
│
├── 📁 docs/                         # Documentación
│   ├── 01_planificacion_analisis.md # (Este documento)
│   ├── 02_arquitectura_diseno.md
│   ├── 03_manual_replicacion.md
│   └── 04_guia_usuario.md
│
├── 📁 tests/                        # Tests
│   ├── 📁 unit/
│   │   └── domain/
│   └── 📁 integration/
│
├── .env.example                     # Variables de entorno (plantilla)
├── .gitignore
├── vercel.json                      # Configuración Vercel
└── README.md
```

### 5.3 Matriz de Trazabilidad Módulo → Requisitos

| Módulo | Requisitos Funcionales | Requisitos No Funcionales |
|--------|------------------------|---------------------------|
| **Dominio** | - | RNF-MANT01, RNF-MANT02, RNF-MANT03 |
| **Aplicación** | RF-M02, RF-M03, RF-M07, RF-S01, RF-S02, RF-S03 | RNF-MANT01 |
| **Infraestructura** | RF-M02, RF-M03 | RNF-SEC01, RNF-PERF02 |
| **Autenticación** | RF-M01, RF-M08 | RNF-SEC01-05 |
| **API** | RF-M02, RF-M03, RF-M04 | RNF-SEC05, RNF-PERF02 |
| **Presentación** | RF-M04, RF-M05, RF-M06, RF-S04, RF-S05 | RNF-UX01-04, RNF-PERF03, RNF-PERF04 |

---

## 6. Análisis de Riesgos

### 6.1 Matriz de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Nivel | Mitigación |
|----|--------|--------------|---------|-------|------------|
| R01 | **Límites de API de Google** — Exceder rate limits | Media | Alto | 🔴 ALTO | Implementar caché en memoria, backoff exponencial |
| R02 | **Cambios en API de Classroom** — Google depreca endpoints | Baja | Muy Alto | 🔴 ALTO | Usar versiones estables, monitorear changelogs |
| R03 | **OAuth mal implementado** — Vulnerabilidades de seguridad | Media | Muy Alto | 🔴 ALTO | Seguir RFC estrictamente, no almacenar tokens en localStorage |
| R04 | **Tokens expirados** — Usuarios deslogueados inesperadamente | Alta | Medio | 🟡 MEDIO | Implementar refresh token, UX clara de re-login |
| R05 | **Rendimiento lento** — Muchos materiales por cargar | Media | Medio | 🟡 MEDIO | Paginación, lazy loading, skeleton loaders |
| R06 | **Usuarios sin cursos** — Edge case no manejado | Media | Bajo | 🟢 BAJO | Diseñar estados vacíos desde el inicio |
| R07 | **Navegadores antiguos** — Incompatibilidad JS moderno | Baja | Bajo | 🟢 BAJO | Definir navegadores soportados, polyfills mínimos |
| R08 | **CORS bloqueado** — Errores de cross-origin | Media | Alto | 🔴 ALTO | Configurar Vercel correctamente, proxy en producción |
| R09 | **Cold start de Vercel** — Primera carga lenta | Media | Medio | 🟡 MEDIO | Optimizar bundle, función de warming |
| R10 | **Credenciales filtradas** — API keys en código | Baja | Muy Alto | 🔴 ALTO | Variables de entorno, auditoría pre-commit |

### 6.2 Detalle de Mitigaciones Críticas

#### R01: Límites de API de Google

```
RIESGO: Google Classroom API tiene límites de 10 requests/segundo/usuario

MITIGACIÓN TÉCNICA:
┌─────────────────────────────────────────────────────────────────┐
│  1. CACHÉ EN MEMORIA (durante la sesión)                        │
│     - Almacenar lista de cursos al obtenerla                    │
│     - Almacenar materiales por curso                            │
│     - TTL: 5 minutos                                            │
│                                                                 │
│  2. BACKOFF EXPONENCIAL                                         │
│     - Si 429, esperar: 1s → 2s → 4s → 8s                        │
│     - Máximo 3 reintentos                                       │
│                                                                 │
│  3. BATCHING                                                    │
│     - Agrupar requests cuando sea posible                       │
│     - No solicitar materiales de cursos no visibles             │
└─────────────────────────────────────────────────────────────────┘

POR QUÉ SÍ: Protege al usuario de errores y mejora la experiencia.
POR QUÉ NO simplemente ignorar: Un 429 puede bloquear al usuario por horas.
```

#### R03: OAuth mal implementado

```
RIESGO: Vulnerabilidades como token leaking, CSRF, session hijacking

MITIGACIÓN TÉCNICA:
┌─────────────────────────────────────────────────────────────────┐
│  ✅ LO QUE HAREMOS:                                             │
│     - Tokens almacenados en cookies HttpOnly + Secure           │
│     - State parameter para prevenir CSRF                        │
│     - PKCE (code_verifier) para apps públicas                   │
│     - Validar tokens en cada request                            │
│                                                                 │
│  ❌ LO QUE NO HAREMOS (ANTI-PATRONES):                          │
│     - ❌ Guardar tokens en localStorage (vulnerable a XSS)      │
│     - ❌ Tokens en URLs (visibles en logs del servidor)         │
│     - ❌ Tokens sin expiración                                  │
│     - ❌ Compartir client_secret en frontend                    │
└─────────────────────────────────────────────────────────────────┘

POR QUÉ SÍ: OAuth2 + PKCE es el estándar de seguridad para SPAs.
POR QUÉ NO localStorage: Cualquier XSS puede robar todos los tokens.
```

#### R10: Credenciales filtradas

```
RIESGO: API keys o secrets hardcodeados y publicados en Git

MITIGACIÓN TÉCNICA:
┌─────────────────────────────────────────────────────────────────┐
│  1. VARIABLES DE ENTORNO                                        │
│     - Toda credencial en .env (nunca en código)                 │
│     - Vercel Environment Variables para producción              │
│                                                                 │
│  2. ARCHIVOS DE EJEMPLO                                         │
│     - .env.example con placeholders: GOOGLE_CLIENT_ID=<tu_id>   │
│     - Documentar en manual de replicación                       │
│                                                                 │
│  3. GITIGNORE ESTRICTO                                          │
│     - .env en .gitignore desde el día 0                         │
│     - Verificar antes de cada commit                            │
│                                                                 │
│  4. PRE-COMMIT HOOKS (Opcional)                                 │
│     - Usar gitleaks o similar para detectar secrets             │
└─────────────────────────────────────────────────────────────────┘

POR QUÉ SÍ: Un secret publicado es irrecuperable (bots lo encuentran en minutos).
POR QUÉ NO "solo tener cuidado": El error humano es inevitable; las herramientas no.
```

### 6.3 Plan de Contingencia

| Escenario | Acción Inmediata | Responsable |
|-----------|------------------|-------------|
| API de Google caída | Mostrar mensaje "Servicio externo no disponible" + datos cacheados | Frontend |
| Token comprometido | Revocar todos los tokens del usuario + forzar re-login | Backend |
| Rate limit alcanzado | Mostrar mensaje + botón "Reintentar en X segundos" | Frontend |
| Deploy fallido | Rollback automático a versión anterior | Vercel |

---

## 📎 Anexos

### Anexo A: Glosario

| Término | Definición |
|---------|------------|
| **OAuth 2.0** | Protocolo estándar de autorización que permite acceso seguro a APIs |
| **Access Token** | Credencial temporal para acceder a recursos protegidos |
| **Refresh Token** | Credencial de larga duración para obtener nuevos access tokens |
| **PKCE** | Proof Key for Code Exchange - Extensión de OAuth para apps públicas |
| **Rate Limit** | Límite de solicitudes por unidad de tiempo impuesto por la API |
| **Serverless** | Modelo donde el proveedor ejecuta código sin gestionar servidores |
| **Clean Architecture** | Patrón que separa código en capas con dependencias hacia adentro |
| **Domain Layer** | Capa con reglas de negocio puras, sin dependencias externas |

### Anexo B: Referencias

1. [Google Classroom API Documentation](https://developers.google.com/classroom/reference/rest)
2. [OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)
3. [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
4. [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
5. [Vercel Serverless Functions](https://vercel.com/docs/functions)

---

## ✅ Checklist de Aprobación

Antes de avanzar a la siguiente fase, verificar:

- [ ] Requisitos funcionales revisados y priorizados
- [ ] Requisitos no funcionales aceptados
- [ ] Historias de usuario con criterios de aceptación
- [ ] Casos de uso con flujos y excepciones
- [ ] Módulos identificados y mapeados
- [ ] Riesgos identificados con mitigaciones
- [ ] Plan de sprints revisado

---

> **Próximo Paso**: Una vez aprobado este documento, se procederá a crear `02_arquitectura_diseno.md` con diagramas técnicos, decisiones de diseño y estructura de código detallada.
