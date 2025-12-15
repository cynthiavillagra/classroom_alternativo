# 🌐 Guía de Deploy Universal

Esta guía explica cómo deployar la aplicación en diferentes entornos manteniendo el mismo código base.

## Principios de Arquitectura Universal

### ✅ El Código NO Debe Saber Dónde Corre

```
❌ MALO: if os.environ.get('VERCEL'): hacer_algo_especial()
✅ BUENO: Código agnóstico que funciona igual en cualquier entorno
```

### ✅ Estado en Cookies, NO en Memoria

```python
# ❌ MALO (no funciona en serverless)
session_store = {}  # Se pierde entre requests

# ✅ BUENO (funciona en cualquier entorno)
access_token = self._get_cookie('access_token')
```

### ✅ Configuración por Variables de Entorno

```python
# ❌ MALO
REDIRECT_URI = "http://localhost:5000/callback"

# ✅ BUENO
REDIRECT_URI = os.getenv("OAUTH_REDIRECT_URI")
```

---

## Desarrollo Local

```bash
# 1. Clonar y configurar
git clone <repo>
cd classroom-explorer
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Configurar variables
cp .env.example .env
# Editar .env con tus credenciales

# 3. Ejecutar
python main.py
# Abrir http://localhost:5000
```

---

## Deploy en Vercel (Serverless)

### Estructura Requerida

```
proyecto/
├── api/
│   └── index.py      # Punto de entrada Vercel
├── public/           # Archivos estáticos
│   ├── index.html
│   ├── dashboard.html
│   └── ...
├── src/              # Código de la aplicación
│   ├── routes/
│   ├── domain/
│   └── ...
├── main.py           # Servidor local + VercelBridge
├── vercel.json       # Configuración Vercel
└── requirements.txt
```

### vercel.json

```json
{
  "functions": {
    "api/index.py": {
      "includeFiles": "../public/**"
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index" },
    { "source": "/dashboard", "destination": "/dashboard.html" },
    { "source": "/login", "destination": "/login.html" },
    { "source": "/materials", "destination": "/materials.html" },
    { "source": "/docs", "destination": "/docs.html" }
  ]
}
```

### api/index.py

```python
from http.server import BaseHTTPRequestHandler
import os, sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from main import VercelBridge
wsgi_app = VercelBridge()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Construir environ WSGI
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': self.path.split('?')[0],
            'QUERY_STRING': self.path.split('?')[1] if '?' in self.path else '',
            'wsgi.input': None,
        }
        # Pasar headers (incluyendo cookies)
        for key, value in self.headers.items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        # Ejecutar y responder
        result = wsgi_app(environ, self._start_response)
        for data in result:
            self.wfile.write(data)
```

### Variables de Entorno en Vercel

En Dashboard > Settings > Environment Variables:

| Variable | Valor |
|----------|-------|
| `GOOGLE_CLIENT_ID` | Tu client ID |
| `GOOGLE_CLIENT_SECRET` | Tu client secret |
| `APP_URL` | `https://tu-app.vercel.app` |
| `OAUTH_REDIRECT_URI` | `https://tu-app.vercel.app/api/auth/callback` |

### Actualizar Google Cloud Console

1. Ir a APIs & Services > Credentials
2. Editar OAuth 2.0 Client
3. Agregar URI de redirección: `https://tu-app.vercel.app/api/auth/callback`
4. Agregar origen autorizado: `https://tu-app.vercel.app`

---

## Deploy en Netlify

### netlify.toml

```toml
[build]
  command = "pip install -r requirements.txt"
  publish = "public"
  functions = "netlify/functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200

[[redirects]]
  from = "/dashboard"
  to = "/dashboard.html"
  status = 200
```

---

## Deploy con Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "main.py"]
```

### docker-compose.yml

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
```

### Ejecutar

```bash
docker-compose up -d
```

---

## Deploy en Servidor Tradicional (VM)

### Con systemd

```bash
# /etc/systemd/system/classroom.service
[Unit]
Description=Classroom Explorer
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/classroom
Environment="PATH=/var/www/classroom/venv/bin"
ExecStart=/var/www/classroom/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Con Nginx (proxy inverso)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Checklist de Deploy Universal

Antes de deployar en cualquier entorno, verifica:

- [ ] **Variables de entorno configuradas**
  - `GOOGLE_CLIENT_ID`
  - `GOOGLE_CLIENT_SECRET`
  - `APP_URL`
  - `OAUTH_REDIRECT_URI`

- [ ] **OAuth configurado en Google Cloud**
  - Redirect URI apunta al nuevo dominio
  - Origen autorizado agregado

- [ ] **Estado NO en memoria**
  - Tokens en cookies
  - Sin variables globales mutables

- [ ] **Código agnóstico**
  - Sin `if VERCEL` o `if LOCAL`
  - Config por env vars

---

## Troubleshooting

### Error: "Invalid state" en OAuth

**Causa**: El state se guardó en memoria y se perdió.
**Solución**: Verificar que state se guarde en cookie.

### Error: "Not authenticated" después de login

**Causa**: access_token se guardó en memoria.
**Solución**: Verificar que access_token se guarde en cookie.

### Error: 404 en archivos estáticos (Vercel)

**Causa**: Vercel no incluye archivos fuera de `api/`.
**Solución**: Agregar `includeFiles` en vercel.json o usar rewrites.

### Error: "No module named 'src'"

**Causa**: Python path no incluye raíz del proyecto.
**Solución**: En api/index.py agregar `sys.path.insert(0, ROOT_DIR)`.
