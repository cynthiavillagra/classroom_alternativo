# Manual Técnico: Configuración Externa — Google OAuth 2.0

## Propósito

**Trazabilidad Completa:**
* **Módulo:** Configuración de Entorno
* **Historia de Usuario:** HU-000 (Setup del proyecto)
* **Criterio de Aceptación:** CA-000.2 (El desarrollador puede obtener credenciales siguiendo la guía)
* **Requisitos:** RF-M01 (Autenticación), RNF-SEG01 (Seguridad)

---

## Estrategia de Construcción Incremental

1. **Validación de Dependencias:** 
   - Depende de: `.env.example` (debe existir primero)
   - POR QUÉ tercero: Después de definir qué variables necesitamos, explicamos cómo obtenerlas

2. **Estructura Base:**
   - Guía paso a paso con instrucciones claras
   - Cada paso numerado y verificable
   - Solución de problemas al final

3. **Lógica Nuclear:**
   - Instrucciones para Google Cloud Console
   - Configuración de OAuth 2.0
   - Scopes necesarios para Classroom API

---

## 📋 Prerrequisitos

- Cuenta de Google (Gmail)
- Acceso a cursos en Google Classroom

---

## 🚀 Paso 1: Crear Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Click en el selector de proyectos (arriba a la izquierda)
3. Click en **"Nuevo Proyecto"**
4. Nombre: `Classroom Explorer` (o el que prefieras)
5. Click **"Crear"**
6. Espera ~30 segundos a que se cree
7. Selecciona el proyecto creado

---

## 🔌 Paso 2: Habilitar APIs Necesarias

1. Ve a **APIs y Servicios** → **Biblioteca**
2. Busca y habilita estas APIs:

| API | Descripción |
|-----|-------------|
| **Google Classroom API** | Acceso a cursos y materiales |
| **Google OAuth 2.0** | Autenticación de usuarios |

Para cada una:
1. Búscala
2. Click en el resultado
3. Click **"Habilitar"**

---

## 🔑 Paso 3: Crear Credenciales OAuth 2.0

### 3.1 Configurar Pantalla de Consentimiento

1. Ve a **APIs y Servicios** → **Pantalla de consentimiento OAuth**
2. Tipo de usuario: **Externo** (a menos que tengas Google Workspace)
3. Click **"Crear"**
4. Completa:
   - **Nombre de la app:** Classroom Explorer
   - **Email de soporte:** Tu email
   - **Logo:** (opcional)
   - **Dominio autorizado:** localhost (para desarrollo)
5. Click **"Guardar y continuar"**

### 3.2 Agregar Scopes

1. Click **"Agregar o quitar scopes"**
2. Busca y agrega estos scopes:

| Scope | Descripción |
|-------|-------------|
| `classroom.courses.readonly` | Ver clases de Google Classroom |
| `classroom.coursework.me.readonly` | Ver tareas y trabajos del curso |
| `classroom.courseworkmaterials.readonly` | Ver materiales de referencia |
| `classroom.announcements.readonly` | Ver publicaciones/anuncios |
| `userinfo.email` | Ver email del usuario |
| `userinfo.profile` | Ver perfil del usuario |

> 📚 **Referencia completa de scopes:** [Google OAuth 2.0 Scopes](https://developers.google.com/identity/protocols/oauth2/scopes?hl=es-419)

3. Click **"Actualizar"** → **"Guardar y continuar"**

### 3.3 Agregar Usuarios de Prueba

1. Click **"Add users"**
2. Agrega tu email de Gmail
3. Click **"Guardar y continuar"**

> ⚠️ **Nota:** En modo de prueba, solo los usuarios agregados pueden usar la app.

### 3.4 Crear Credenciales

1. Ve a **APIs y Servicios** → **Credenciales**
2. Click **"Crear credenciales"** → **"ID de cliente OAuth"**
3. Tipo de aplicación: **Aplicación web**
4. Nombre: `Classroom Explorer Web`
5. **URIs de redirección autorizados:**
   - Para desarrollo: `http://localhost:5000/api/auth/callback`
   - Para producción: `https://tu-dominio.com/api/auth/callback`
6. Click **"Crear"**

### 3.5 Copiar Credenciales

Aparecerá un popup con:
- **ID de cliente:** `xxxx.apps.googleusercontent.com`
- **Secreto de cliente:** `GOCSPX-xxxx`

> 🔒 **CRÍTICO:** Guarda estos valores. El secreto NO se puede ver de nuevo.

---

## 📝 Paso 4: Configurar Variables de Entorno

1. Copia el archivo `.env.example`:
```powershell
copy .env.example .env
```

2. Edita `.env` con tus valores:
```env
GOOGLE_CLIENT_ID=tu_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-tu_client_secret
OAUTH_REDIRECT_URI=http://localhost:5000/api/auth/callback
APP_URL=http://localhost:5000
SESSION_SECRET=genera_un_token_aleatorio
ENVIRONMENT=development
```

3. Genera el SESSION_SECRET:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## ✅ Paso 5: Verificar Configuración

1. Inicia el servidor:
```powershell
python main.py
```

2. Abre http://localhost:5000

3. Click en "Comenzar con Google"

4. Deberías ver la pantalla de consentimiento de Google

5. Acepta los permisos

6. Serás redirigido al dashboard

---

## 🐛 Solución de Problemas

### Error: "redirect_uri_mismatch"
- Verifica que la URI en Google Cloud Console coincida **exactamente** con `OAUTH_REDIRECT_URI`
- Incluye el protocolo (http:// o https://)

### Error: "access_denied"
- Verifica que tu email esté en la lista de "Usuarios de prueba"
- O publica la app (requiere verificación de Google)

### Error: "invalid_client"
- Verifica que `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` estén correctos
- Regenera las credenciales si es necesario

### Error: "API not enabled"
- Ve a la Biblioteca de APIs y habilita Google Classroom API

### Error: "403 Forbidden" en materiales o anuncios
- Verifica que agregaste los scopes correctos en Google Cloud Console
- Cierra sesión y vuelve a iniciar para que Google pida los nuevos permisos

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ OAuth 2.0 de Google

| Beneficio | Explicación |
|-----------|-------------|
| **Seguridad** | No guardamos contraseñas |
| **Confianza** | Los usuarios confían en Google |
| **Scopes** | Control granular de permisos |
| **Gratis** | No hay costo por autenticación |

### ❌ POR QUÉ NO implementar login propio

| Riesgo | Impacto |
|--------|---------|
| **Seguridad** | Manejo de passwords es complejo |
| **Mantenimiento** | Reset de contraseña, 2FA, etc. |
| **Confianza** | Usuarios dudan de dar passwords a apps nuevas |

---

## Prueba de Fuego

1. Sigue los pasos del archivo
2. Verifica que puedas iniciar sesión con Google
3. Esperado: Redirigido a dashboard tras login
4. Verifica que puedas ver cursos, tareas, materiales y anuncios

---

## 🤖 AI Stack

Generado mediante metodología SDLC V5 usando Google Antigravity + Claude Opus 4.5
