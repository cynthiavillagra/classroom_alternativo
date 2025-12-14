# 📄 Auth Handler — Manual Técnico

**Archivo:** `api/routes/auth.py`  
**Propósito:** Endpoints de autenticación con Google OAuth 2.0 usando Python POO puro  
**Trazabilidad:** RF-M01 (Autenticación), RNF-SEG01 (Seguridad), OAuth 2.0

---

## ⚠️ [REFACTOR] Cambio de Flask a Python POO

**Razón del cambio:** El requisito especifica "Python POO sin frameworks externos".

| Antes | Después |
|-------|---------|
| Flask Blueprint | http.server (librería estándar) |
| flask.session | SessionStore (clase propia) |
| requests | http.client (librería estándar) |

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar SOLO librería estándar:**
   - `http.server`: Servidor HTTP de Python
   - `urllib.parse`: Parseo de URLs
   - `http.client`: Cliente HTTP para llamar a Google
   - `ssl`: Conexiones HTTPS seguras
   - POR QUÉ NO requests: Es una dependencia externa

2. **Paso 2 — Clase SessionStore (POO):**
   - Almacén de sesiones en memoria
   - Métodos: `create_session()`, `get()`, `set()`, `delete()`
   - POR QUÉ clase propia: Sin Flask.session, implementamos nuestra propia

3. **Paso 3 — Clase AuthHandler (herencia POO):**
   - Hereda de `BaseHTTPRequestHandler`
   - Implementa `do_GET()` como template method
   - Router manual basado en `self.path`
   - POR QUÉ herencia: Patrón Template Method de la stdlib

4. **Paso 3.1-3.5 — Métodos de rutas:**
   - `_handle_login()`: Genera state, redirige a Google
   - `_handle_callback()`: Valida state, intercambia code→token
   - `_handle_logout()`: Limpia sesión
   - `_handle_me()`: Retorna info del usuario

5. **Paso 4 — Helpers HTTP:**
   - `_send_json_response()`: Respuesta JSON
   - `_send_redirect()`: Redirección HTTP 302
   - `_exchange_code_for_token()`: POST a Google con http.client
   - `_get_user_id()`: GET userinfo con http.client

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque valida que las clases POO están correctamente definidas y que NO se usa Flask. No levanta servidor HTTP real.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 2: Clase de sesión (POO pura, sin Flask)
# ═══════════════════════════════════════════════════════════════
class SessionStore:
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self) -> str:
        session_id = secrets.token_urlsafe(32)
        self._sessions[session_id] = {}
        return session_id


# ═══════════════════════════════════════════════════════════════
# Paso 3: Handler HTTP (herencia de librería estándar)
# ═══════════════════════════════════════════════════════════════
class AuthHandler(BaseHTTPRequestHandler):
    """
    Hereda de BaseHTTPRequestHandler (Python estándar).
    Patrón Template Method: do_GET se llama automáticamente.
    """
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/auth/login':
            self._handle_login()
        elif path == '/api/auth/callback':
            self._handle_callback(query)
        # ... más rutas
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.routes.auth
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: Auth Handler (Python POO puro)
============================================================

1. Verificar SessionStore (POO):
   ✓ Sesión creada: ...
   ✓ set() funciona
   ✓ get() retorna: test_value
   ✓ delete() funciona

2. Verificar AuthHandler (herencia POO):
   ✓ Clase: AuthHandler
   ✓ Hereda de: BaseHTTPRequestHandler
   ✓ Método do_GET: True

4. Verificar que es Python puro (sin Flask):
   ✓ Flask en sys.modules: False (esperado: False)
   ✓ ¡Confirmado: NO usa Flask!

✅ Prueba de Auth Handler (POO puro): OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ Python POO puro

| Beneficio | Explicación |
|-----------|-------------|
| **Sin dependencias** | Solo usa librería estándar de Python |
| **Educativo** | Muestra cómo funciona HTTP internamente |
| **Control total** | Sin abstracciones de frameworks |
| **Portable** | Funciona en cualquier Python 3.x |

### ❌ POR QUÉ NO usar Flask (como estaba antes)

| Razón | Detalle |
|-------|---------|
| **Requisito explícito** | "Python POO sin frameworks" |
| **Dependencia externa** | Requiere `pip install flask` |
| **Oculta complejidad** | No aprenderíamos HTTP real |

---

## 🎓 Conceptos Educativos

### Patrón Template Method (Herencia)

`BaseHTTPRequestHandler` implementa el patrón Template Method:
- La clase base maneja el socket HTTP
- Nosotros sobreescribimos `do_GET()`, `do_POST()`
- La clase base llama nuestros métodos automáticamente

```python
class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # Llamado automáticamente en GET requests
        ...
```

### Sesiones sin Framework

Sin Flask.session, implementamos nuestra propia:

```python
class SessionStore:
    _sessions = {}  # En memoria
    
    def create_session(self) -> str:
        sid = secrets.token_urlsafe(32)
        self._sessions[sid] = {}
        return sid
```

La cookie `session_id` se envía al cliente, y la buscamos en cada request.
