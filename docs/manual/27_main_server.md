# Manual Técnico: main.py

## Propósito

**Trazabilidad Completa:**
* **Módulo:** Server Entrypoint
* **Historia de Usuario:** HU-000 (Setup - levantar servidor local)
* **Criterio de Aceptación:** CA-000.1 (El servidor responde en localhost:5000)

---

## Estrategia de Construcción Incremental

1. **Validación de Dependencias:**
   - `http.server.HTTPServer`: Servidor HTTP de Python estándar
   - `BaseHTTPRequestHandler`: Clase base para manejar requests
   - Handlers de `api.routes`: AuthHandler, CoursesHandler, MaterialsHandler
   - POR QUÉ no uvicorn: Es dependencia externa

2. **Estructura Base:**
   - Clase `MainRouter` que hereda de `BaseHTTPRequestHandler`
   - Método `do_GET()` como router principal
   - Función `run_server()` para iniciar

3. **Lógica Nuclear:**
   - Parsear path del request
   - Delegar a handler especializado según prefijo de ruta
   - Servir archivos estáticos para frontend
   - Responder 404 para rutas no encontradas

---

## Aclaración Metodológica: Rol del Bloque Main

*El bloque main tiene dos modos:*
- `python main.py --test` → Prueba atómica (verifica imports)
- `python main.py` → Inicia servidor real

---

## Código Fuente (Fragmento Clave)

```python
class MainRouter(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path.startswith('/api/auth/'):
            self._delegate_to_auth()
        elif '/materials' in path:
            self._delegate_to_materials()
        elif path.startswith('/api/courses'):
            self._delegate_to_courses()
        elif path == '/':
            self._serve_static('public/index.html', 'text/html')
        else:
            self._send_not_found()

def run_server(host='localhost', port=5000):
    httpd = HTTPServer((host, port), MainRouter)
    httpd.serve_forever()
```

---

## Prueba de Fuego

### 1. Prueba Atómica (imports)
```powershell
python main.py --test
```

**Salida esperada:**
```
✅ Prueba de Main Server: OK
```

### 2. Prueba de Recorrido (servidor real)
```powershell
# Terminal 1: Iniciar servidor
python main.py

# Terminal 2: Probar endpoint
curl http://localhost:5000/api/auth/me
```

**Salida esperada del curl:**
```json
{"authenticated": false}
```

---

## Análisis Dual

### Por qué SÍ:
- **Python POO puro**: Sin frameworks externos
- **Router central**: Un punto de entrada que delega
- **Archivos estáticos**: Sirve frontend HTML/CSS/JS
- **Configurable**: host/port como parámetros
- **[REFACTOR] VercelBridge**: Compatibilidad con Vercel sin frameworks

### Por qué NO (riesgos):
- **Sin router central**: Múltiples servidores escuchando
- **Sin delegación**: Todo el código en un archivo gigante
- **Framework externo**: Viola requisito POO pura
- **Sin VercelBridge**: Vercel no puede ejecutar HTTPServer.serve_forever()

---

## 🔧 Guía de Resolución de Problemas (Troubleshooting)

### 1. Diferencias de Entorno

| Entorno | Método | Explicación |
|---------|--------|-------------|
| **Local** | `HTTPServer.serve_forever()` | Servidor TCP tradicional que mantiene conexión abierta |
| **Vercel** | `app(environ, start_response)` | Función WSGI que se ejecuta por cada request |

**Por qué la diferencia:**
- Vercel es serverless: no hay un servidor "siempre encendido"
- Cada request crea una nueva instancia de la función
- `serve_forever()` bloqueante causa timeout en Vercel

### 2. Errores Comunes

#### "Missing variable 'app'"
```
Error: Cannot find module handler "main.app"
```
**Causa:** Vercel busca una variable `app` que implemente WSGI.

**Solución:** Verificar que `main.py` tiene:
```python
app = VercelBridge()
```

#### "Error de Credenciales (400/401)"
```
Error: invalid_client o access_denied
```
**Causa:** Variables de entorno no configuradas.

**Solución:**
1. Verificar que `.env` existe con valores reales
2. En Vercel: Settings → Environment Variables
3. Diagnóstico rápido:
```python
import os
print("CLIENT_ID:", os.getenv('GOOGLE_CLIENT_ID'))
```

#### "⚠️ ALERTA: Variable X no configurada"
**Causa:** El diagnóstico de arranque detectó variables faltantes.

**Solución:**
1. Local: Crear `.env` con valores de `.env.example`
2. Vercel: Configurar en Dashboard → Settings → Environment Variables

#### "Despliegue Fantasma" (Vercel no detecta cambios)
**Síntoma:** El código cambió pero Vercel sirve la versión antigua.

**Solución:**
```powershell
# Forzar nuevo commit
git commit --allow-empty -m "force: trigger deploy"
git push

# O crear deployment manual
vercel --prod --force
```

### 3. Verificación de Deploy

```powershell
# Probar local
python main.py --test

# Probar Vercel local
vercel dev

# Probar producción
curl https://tu-app.vercel.app/api/auth/me
```

---

## 🤖 AI Stack

Generado mediante metodología SDLC V5 usando Google Antigravity + Claude Opus 4.5

