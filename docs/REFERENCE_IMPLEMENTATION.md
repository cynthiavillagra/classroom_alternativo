# 📘 Implementación de Referencia: Classroom Explorer

Este documento complementa `PROMPTS_MAESTROS_V2.md` con las respuestas específicas y decisiones tomadas para este proyecto. Usar ambos documentos permite replicar el proyecto completo.

---

## 🎯 Respuestas a la Entrevista Técnica (PROMPT 0)

```
1. Problema/Usuario:
   - Problema: La interfaz de Google Classroom es lenta y no permite
     filtrar materiales fácilmente.
   - Usuario: Estudiantes y profesores que usan Google Classroom.
   - Solución: Vista alternativa que lista todos los materiales con filtros.

2. Tipo de App: [X] Web con backend (Python)

3. Persistencia: [X] API externa como storage (Google Classroom API)

4. Autenticación: [X] OAuth (Google)

5. APIs Externas: [X] Google APIs
   - Google Classroom API (courses, courseWork, courseWorkMaterials, announcements)
   - Google OAuth 2.0

6. Despliegue: [X] Vercel + [X] Docker + [X] Local
   (Arquitectura universal)

7. Roles: Todos iguales (cada usuario ve sus propios cursos)

8. Stack preferido: Python POO PURO (sin frameworks como Flask/Django)

9. Budget: Solo herramientas gratuitas

10. Prioridad: MVP rápido pero con arquitectura limpia
```

---

## 🏗️ Decisiones Arquitectónicas Clave

### 1. Python POO Puro (Sin Frameworks)

**Decisión:** Usar `http.server.BaseHTTPRequestHandler` en lugar de Flask/FastAPI.

**POR QUÉ SÍ:**
- Objetivo educativo: enseñar HTTP desde cero
- Sin dependencias externas pesadas
- Control total del flujo

**POR QUÉ NO Flask:**
- Es un framework externo
- Oculta la mecánica de HTTP
- Viola el requisito educativo

**Código clave:**
```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class MainRouter(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path.startswith('/api/auth'):
            self._delegate_to_auth()
        elif path.startswith('/api/courses'):
            self._delegate_to_courses()
        # ...
```

### 2. Estado en Cookies (Stateless)

**Decisión:** Guardar `access_token` en cookie HttpOnly, no en memoria.

**POR QUÉ SÍ:**
- Funciona en serverless (Vercel, Lambda)
- Cada request es independiente
- Escala horizontalmente

**POR QUÉ NO session_store en memoria:**
- En serverless, cada request puede ir a distinta instancia
- La memoria se pierde entre requests
- No escala

**Código clave:**
```python
# En callback de OAuth:
self.send_header('Set-Cookie', f'access_token={access_token}; HttpOnly; Path=/; SameSite=Lax')

# En handlers:
access_token = self._get_cookie('access_token')
```

### 3. VercelBridge (Adaptador WSGI)

**Decisión:** Crear un adaptador que traduce requests Vercel a nuestro handler.

**POR QUÉ SÍ:**
- El mismo código funciona local y en Vercel
- Separation of Concerns
- Fácil de adaptar a otras plataformas

**Código clave:**
```python
class VercelBridge:
    """Adaptador WSGI para Vercel Serverless."""
    
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        # Crear FakeHandler que simula request HTTP
        handler = FakeHandler(path, environ)
        handler.do_GET()
        # Devolver respuesta WSGI
        start_response(status, headers)
        return [body]
```

### 4. Archivos Estáticos por Plataforma

**Decisión:** En producción, los archivos estáticos los sirve la plataforma (Vercel CDN), no la función.

**POR QUÉ SÍ:**
- Más rápido (CDN)
- Menos carga en función serverless
- Estándar de la industria

**vercel.json clave:**
```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index" },
    { "source": "/dashboard", "destination": "/dashboard.html" },
    { "source": "/login", "destination": "/login.html" }
  ]
}
```

---

## 📁 Estructura de Carpetas

```
proyecto/
├── api/                      # Entry point para Vercel
│   └── index.py              # Único archivo, importa de main.py
│
├── src/                      # Código de la aplicación
│   ├── domain/               # Capa de Dominio (POO pura)
│   │   ├── entities/         # Course, Material, MaterialType
│   │   ├── factories/        # CourseFactory, MaterialFactory
│   │   └── interfaces/       # IClassroomRepository (abstracto)
│   │
│   ├── application/          # Capa de Aplicación
│   │   ├── use_cases/        # ListUserCourses, ListCourseMaterials
│   │   └── filters/          # MaterialFilter, estrategias
│   │
│   ├── infrastructure/       # Capa de Infraestructura
│   │   ├── repositories/     # GoogleClassroomRepository
│   │   ├── mappers/          # ClassroomMapper
│   │   ├── config.py         # Config desde env vars
│   │   └── google_classroom_client.py
│   │
│   └── routes/               # Handlers HTTP (Presentation)
│       ├── auth.py           # OAuth flow
│       ├── courses.py        # /api/courses
│       └── materials.py      # /api/courses/{id}/materials
│
├── public/                   # Frontend (estáticos)
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── materials.html
│   ├── css/
│   └── js/
│
├── main.py                   # Servidor local + VercelBridge
├── vercel.json               # Config Vercel
├── requirements.txt
└── .env.example
```

---

## 🔐 OAuth Flow Completo

### Flujo Visual

```
Usuario → /login → Google Auth → /api/auth/callback → /dashboard
              ↓                        ↓
         Guarda state            Intercambia code
         en cookie               por token
              ↓                        ↓
         Redirige a              Guarda token
         Google                  en cookie
```

### Código del Callback (Stateless)

```python
def _handle_callback(self):
    # 1. Validar state desde cookie (no memoria)
    state = query.get('state', [None])[0]
    stored_state = self._get_cookie('oauth_state')
    
    if state != stored_state:
        return self._send_error('Invalid state')
    
    # 2. Intercambiar code por token
    code = query.get('code')[0]
    token_data = self._exchange_code_for_token(code)
    access_token = token_data['access_token']
    
    # 3. Guardar en cookie (NO en memoria)
    self.send_response(302)
    self.send_header('Location', '/dashboard')
    self.send_header('Set-Cookie', f'access_token={access_token}; HttpOnly; Path=/')
    self.send_header('Set-Cookie', 'oauth_state=; Max-Age=0')  # Limpiar
    self.end_headers()
```

---

## 🎨 Google Classroom API - Scopes Requeridos

```python
SCOPES = [
    # Ver lista de cursos
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    
    # Ver tareas y materiales
    'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
    
    # Ver materiales adicionales
    'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
    
    # Ver anuncios
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    
    # Ver perfil básico
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]
```

**Documentación oficial:** https://developers.google.com/classroom/reference/rest

---

## 🧪 Tests E2E Manuales (Orden Recomendado)

### Test 1: Flujo de Login

```
1. Abrir http://localhost:5000/login
2. Click "Iniciar sesión con Google"
3. Seleccionar cuenta
4. Aceptar permisos
5. ESPERADO: Redirige a /dashboard con nombre visible
```

### Test 2: Ver Cursos

```
1. En /dashboard
2. ESPERADO: Lista de cursos del usuario
3. Verificar: Nombre del curso, sección, estado
```

### Test 3: Ver Materiales

```
1. Click en un curso
2. ESPERADO: Lista de materiales (tareas, recursos, anuncios)
3. Verificar: Filtros por tipo funcionan
```

### Test 4: Logout

```
1. Click "Cerrar sesión"
2. ESPERADO: Redirige a /login
3. Verificar: Cookies limpiadas (DevTools > Application > Cookies)
```

### Test 5: Acceso sin Login

```
1. Borrar cookies
2. Ir a /api/courses
3. ESPERADO: 401 Unauthorized
```

---

## ⚠️ Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `Invalid state` | State en memoria (serverless) | Guardar state en cookie |
| `Not authenticated` post-login | Token en memoria | Guardar token en cookie |
| `404` en `/dashboard` (Vercel) | Archivos no incluidos | Usar rewrites en vercel.json |
| `No module named 'src'` | Path incorrecto | `sys.path.insert(0, ROOT_DIR)` |
| `403 Forbidden` en API | Scope faltante | Agregar scope, re-autorizar usuario |
| `TypeError: datetime` | Comparar naive vs aware | Usar `datetime.now(timezone.utc)` |

---

## 📚 Secuencia de Desarrollo Recomendada

Usando PROMPTS_MAESTROS_V2:

1. **PROMPT 0** - Entrevista (usar respuestas de arriba)
2. **PROMPT 1** - Planificación
3. **PROMPT 2** - Diseño (crear estructura de carpetas)
4. **PROMPT 3** - Implementación
   - 3.1: Domain Layer (entities)
   - 3.2: Infrastructure Layer (Google client, repository)
   - 3.3: Application Layer (use cases)
   - 3.4: Presentation Layer (routes, main.py)
   - 3.5: Frontend (HTML/CSS/JS)
5. **PROMPT 4** - Testing (E2E manual primero)
6. **PROMPT 5** - Deploy (usar DEPLOY_UNIVERSAL.md)

---

## 🔗 Referencias

| Documento | Propósito |
|-----------|-----------|
| `docs/PROMPTS_MAESTROS_V2.md` | Metodología universal |
| `docs/DEPLOY_UNIVERSAL.md` | Guía de deploy multi-plataforma |
| `docs/manual/` | Manuales paso a paso |
| Este documento | Decisiones específicas de este proyecto |

---

**Con estos 4 documentos puedes replicar Classroom Explorer desde cero.**
