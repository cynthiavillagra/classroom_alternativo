# 🔐 Guía de Configuración Externa — Google OAuth 2.0

**Archivo:** `docs/setup_externo.md`  
**Propósito:** Instrucciones paso a paso para obtener credenciales de Google Cloud Console  
**Trazabilidad:** RF-M01 (Autenticación), RNF-SEG01 (Seguridad)

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

```
https://www.googleapis.com/auth/classroom.courses.readonly
https://www.googleapis.com/auth/classroom.course-work.readonly
https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
```

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

## 🤖 AI Stack

Generado mediante metodología SDLC V5 usando Google Antigravity + Claude Opus 4.5
