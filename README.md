# 📚 Classroom Explorer

> **Explorador avanzado de materiales de Google Classroom**

Una aplicación web que permite visualizar, filtrar y organizar los materiales de tus cursos de Google Classroom de forma más eficiente que la interfaz nativa.

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
│  API Layer (Flask - Vercel Serverless)                      │
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
# Desarrollo
python -m flask --app api/main run --debug

# La app estará en http://localhost:5000
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

## 🚀 Deploy a Vercel

### 1. Instalar Vercel CLI

```bash
npm install -g vercel
```

### 2. Login

```bash
vercel login
```

### 3. Configurar Variables de Entorno

En el dashboard de Vercel:
1. Ve a **Settings** → **Environment Variables**
2. Agrega todas las variables de `.env`
3. Asegúrate de cambiar `OAUTH_REDIRECT_URI` a tu dominio de producción

### 4. Deploy

```bash
vercel --prod
```

---

## 📚 Documentación

- [Planificación y Análisis](docs/01_planificacion_analisis.md)
- [Arquitectura y Patrones](docs/02_a_arquitectura_patrones.md)
- [Modelado de Datos](docs/02_b_modelado_datos.md)
- [API y Dinámica](docs/02_c_api_dinamica.md)
- [Estrategia de Datos](docs/03_estrategia_datos.md)

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Justificación |
|------|------------|---------------|
| **Frontend** | HTML/CSS/JS Vanilla | Simplicidad, sin dependencias |
| **Backend** | Python 3.11+ | Claridad sintáctica, ideal para POO |
| **Framework** | Flask | Ligero, compatible con Vercel |
| **Autenticación** | Google OAuth 2.0 | Estándar de la industria |
| **API Externa** | Google Classroom API | Fuente de datos |
| **Deploy** | Vercel Serverless | Sin servidor, escalable |

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
- [Flask Documentation](https://flask.palletsprojects.com/)
