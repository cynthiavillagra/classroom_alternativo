# 📚 Classroom Explorer

> **Explorador avanzado de materiales de Google Classroom**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Tests](https://img.shields.io/badge/Tests-39%20passed-success)
![Architecture](https://img.shields.io/badge/Architecture-Clean%20POO-purple)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green)

Una aplicación web que permite visualizar, filtrar y organizar los materiales de tus cursos de Google Classroom de forma más eficiente que la interfaz nativa.

**Python POO Puro** — Sin frameworks web externos (Flask, FastAPI, Django).

---

## 🎯 Características

- ✅ **Autenticación con Google** — Login seguro con OAuth 2.0
- 📚 **Vista de Cursos** — Lista todos tus cursos activos
- 📄 **Explorador de Materiales** — Visualiza todos los materiales de tus cursos
- 🔍 **Filtros Avanzados** — Filtra por tipo, curso, fecha
- 🎨 **Vistas Múltiples** — Alterna entre vista lista y tarjetas
- 🚀 **Rápido y Ligero** — Sin base de datos, datos directos de Google API

---

## 🏗️ Arquitectura

Este proyecto sigue **Clean Architecture** con las siguientes capas:

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (HTML/CSS/JS Vanilla)                             │
├─────────────────────────────────────────────────────────────┤
│  API Layer (Python POO Puro + VercelBridge)                 │
├─────────────────────────────────────────────────────────────┤
│  Application Layer (Use Cases)                              │
├─────────────────────────────────────────────────────────────┤
│  Domain Layer (Entities - POO Pura)                         │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (Google Classroom Client)             │
└─────────────────────────────────────────────────────────────┘
```

**Patrones de Diseño Aplicados:**
- Repository Pattern
- Adapter Pattern
- Dependency Injection
- Factory Pattern
- Strategy Pattern (Filtros)

---

## 🚀 Setup Local

### Prerrequisitos

- Python 3.11 o superior
- Cuenta de Google con acceso a Classroom
- Credenciales OAuth 2.0 de Google Cloud Console

### 1. Clonar el Repositorio

```bash
git clone <tu-repo-url>
cd app-classroom
```

### 2. Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

# Activar (Mac/Linux)
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# (Ver sección "Obtener Credenciales de Google" abajo)
```

### 5. Ejecutar en Local

```bash
# Iniciar servidor
python main.py

# La app estará en http://localhost:5000

# Para pruebas atómicas
python main.py --test
```

---

## 🔐 Obtener Credenciales de Google

### Paso 1: Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las siguientes APIs:
   - Google Classroom API
   - Google OAuth 2.0

### Paso 2: Crear Credenciales OAuth 2.0

1. Ve a **APIs & Services** → **Credentials**
2. Click en **Create Credentials** → **OAuth 2.0 Client ID**
3. Tipo de aplicación: **Web application**
4. Nombre: `Classroom Explorer`
5. **Authorized redirect URIs**:
   - Para local: `http://localhost:5000/api/auth/callback`
   - Para producción: `https://tu-dominio.vercel.app/api/auth/callback`
6. Click en **Create**
7. Copia el **Client ID** y **Client Secret**

### Paso 3: Configurar .env

```env
GOOGLE_CLIENT_ID=tu_client_id_aqui
GOOGLE_CLIENT_SECRET=tu_client_secret_aqui
OAUTH_REDIRECT_URI=http://localhost:5000/api/auth/callback
APP_URL=http://localhost:5000
SESSION_SECRET=genera_un_secret_aleatorio_de_64_caracteres
ENVIRONMENT=development
```

**Generar SESSION_SECRET:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📁 Estructura del Proyecto

```
app-classroom/
├── api/                          # Backend (Python)
│   ├── domain/                   # Capa de Dominio (POO pura)
│   │   ├── entities/             # Entidades: Course, Material
│   │   ├── factories/            # Factories para crear entidades
│   │   └── interfaces/           # Interfaces (Ports)
│   ├── application/              # Capa de Aplicación (Use Cases)
│   │   ├── use_cases/            # Casos de uso
│   │   └── filters/              # Estrategias de filtrado
│   ├── infrastructure/           # Capa de Infraestructura
│   │   ├── repositories/         # Implementaciones de repositorios
│   │   ├── mappers/              # Adaptadores API → Domain
│   │   ├── config.py             # Configuración
│   │   ├── cache.py              # Caché en memoria
│   │   └── google_classroom_client.py
│   └── routes/                   # Endpoints API (Flask)
│       ├── auth.py
│       ├── courses.py
│       └── materials.py
├── public/                       # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── login.html
│   ├── css/
│   └── js/
├── docs/                         # Documentación
│   ├── 01_planificacion_analisis.md
│   ├── 02_a_arquitectura_patrones.md
│   ├── 02_b_modelado_datos.md
│   ├── 02_c_api_dinamica.md
│   └── 03_estrategia_datos.md
├── tests/                        # Tests
│   ├── unit/
│   └── integration/
├── .env.example                  # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt              # Dependencias Python
├── vercel.json                   # Configuración de Vercel
└── README.md                     # Este archivo
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=api --cov-report=html

# Solo tests unitarios
pytest tests/unit/

# Solo tests de integración
pytest tests/integration/
```

---

## 🚀 Deploy

### Arquitectura Universal

Este proyecto está diseñado para funcionar en **cualquier entorno**:

| Entorno | Configuración |
|---------|---------------|
| **Local** | `python main.py` |
| **Vercel** | Conectar repo, listo |
| **Docker** | `docker-compose up` |
| **Netlify** | Usar `netlify.toml` |
| **Servidor** | Con systemd + nginx |

**Ver guía completa:** [`docs/DEPLOY_UNIVERSAL.md`](docs/DEPLOY_UNIVERSAL.md)

### Deploy a Vercel (Recomendado)

1. **Conectar repositorio a Vercel**
   - Ir a [vercel.com](https://vercel.com)
   - Import Git Repository
   - Seleccionar tu repo

2. **Configurar Variables de Entorno**

   En Dashboard > Settings > Environment Variables:

   | Variable | Valor |
   |----------|-------|
   | `GOOGLE_CLIENT_ID` | Tu client ID |
   | `GOOGLE_CLIENT_SECRET` | Tu client secret |
   | `APP_URL` | `https://tu-app.vercel.app` |
   | `OAUTH_REDIRECT_URI` | `https://tu-app.vercel.app/api/auth/callback` |

3. **Actualizar Google Cloud Console**
   - Agregar `https://tu-app.vercel.app/api/auth/callback` a Redirect URIs
   - Agregar `https://tu-app.vercel.app` a Authorized Origins

4. **Deploy automático**
   - Cada `git push` deploya automáticamente

---

## 📚 Documentación

### Documentación de Diseño
- [Planificación y Análisis](docs/01_planificacion_analisis.md)
- [Arquitectura y Patrones](docs/02_a_arquitectura_patrones.md)
- [Modelado de Datos](docs/02_b_modelado_datos.md)
- [API y Dinámica](docs/02_c_api_dinamica.md)
- [Estrategia de Datos](docs/03_estrategia_datos.md)
- [**Deploy Universal**](docs/DEPLOY_UNIVERSAL.md) — **Nuevo: Deploy en cualquier plataforma**

### Manuales Técnicos (Para Replicar el Proyecto)
- [📚 Índice de Manuales](docs/00_indice_manuales.md) — **Sigue la secuencia 01-21 para construir todo desde cero**
- Los manuales están en `docs/manual/` con formato `NN_nombre.md`
- Cada manual tiene "Prueba de Fuego" con comando exacto y salida esperada

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Justificación |
|------|------------|---------------|
| **Frontend** | HTML/CSS/JS Vanilla | Simplicidad, sin dependencias |
| **Backend** | Python 3.11+ POO Puro | Sin frameworks web (universal) |
| **Servidor** | http.server + VercelBridge | Funciona en cualquier entorno |
| **Autenticación** | Google OAuth 2.0 | Estándar de la industria |
| **API Externa** | Google Classroom API | Fuente de datos |
| **Estado** | Cookies (stateless) | Funciona en serverless |
| **Deploy** | Vercel / Docker / Cualquiera | Arquitectura universal |

---

## 🤝 Contribuir

Este es un proyecto educativo para aprender Clean Architecture y POO.

**Áreas de mejora futuras:**
- [ ] Agregar favoritos (requiere Supabase)
- [ ] Historial de búsquedas
- [ ] Modo oscuro
- [ ] Búsqueda full-text
- [ ] Notificaciones de nuevos materiales

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

Desarrollado como proyecto educativo para aprender:
- Clean Architecture
- Programación Orientada a Objetos (POO)
- Patrones de Diseño
- Integración con APIs externas
- OAuth 2.0

---

## 🙏 Agradecimientos

- [Google Classroom API Documentation](https://developers.google.com/classroom)
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Documentation](https://docs.python.org/3/)

---

## 🤖 AI Stack

> Generado mediante metodología **SDLC V5** usando **Google Antigravity + Claude Opus 4.5**.

Este proyecto fue desarrollado con asistencia de IA siguiendo:
- Metodología de desarrollo incremental con pruebas atómicas
- Documentación técnica con trazabilidad completa
- Checkpoints de persistencia para continuidad entre sesiones

