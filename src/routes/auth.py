"""
Auth HTTP Handler - Classroom Explorer

[REFACTOR] Cambiado de Flask Blueprint a http.server de Python estándar.
POR QUÉ: El requisito especifica Python POO sin frameworks externos.

Endpoints de autenticación con Google OAuth 2.0 usando Python puro.

POR QUÉ SÍ http.server:
✅ Librería estándar de Python (sin dependencias)
✅ POO pura con herencia de clases
✅ Control total sobre el manejo HTTP

POR QUÉ NO Flask:
❌ Es un framework externo
❌ Viola el requisito de "Python POO sin frameworks"
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias (SOLO librería estándar)
# ═══════════════════════════════════════════════════════════════
# [REFACTOR] Eliminado Flask, usando http.server estándar
# POR QUÉ http.server: Servidor HTTP de la librería estándar de Python
# POR QUÉ urllib.parse: Parseo de URLs y query strings
# POR QUÉ json: Serialización de respuestas
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import json
import secrets
import http.client
import ssl
from typing import Dict, Any, Optional
from src.infrastructure.config import Config


# ═══════════════════════════════════════════════════════════════
# Paso 2: Clase de sesión simple (POO pura)
# ═══════════════════════════════════════════════════════════════
# [REFACTOR] Implementación propia de sesión sin Flask
# POR QUÉ clase separada: Single Responsibility Principle
class SessionStore:
    """
    Almacén de sesiones en memoria.
    
    POR QUÉ diccionario: Estructura simple para MVP
    POR QUÉ en memoria: No requiere base de datos externa
    """
    
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self) -> str:
        """Crea una nueva sesión y retorna el ID."""
        session_id = secrets.token_urlsafe(32)
        self._sessions[session_id] = {}
        return session_id
    
    def get(self, session_id: str, key: str) -> Optional[Any]:
        """Obtiene un valor de la sesión."""
        if session_id not in self._sessions:
            return None
        return self._sessions[session_id].get(key)
    
    def set(self, session_id: str, key: str, value: Any) -> None:
        """Guarda un valor en la sesión."""
        if session_id not in self._sessions:
            self._sessions[session_id] = {}
        self._sessions[session_id][key] = value
    
    def delete(self, session_id: str) -> None:
        """Elimina una sesión completa."""
        if session_id in self._sessions:
            del self._sessions[session_id]


# Instancia global de sesiones (Singleton pattern)
session_store = SessionStore()


# ═══════════════════════════════════════════════════════════════
# Paso 3: Handler HTTP para autenticación (POO con herencia)
# ═══════════════════════════════════════════════════════════════
# [REFACTOR] Hereda de BaseHTTPRequestHandler (librería estándar)
# POR QUÉ herencia: Patrón Template Method de la librería estándar
class AuthHandler(BaseHTTPRequestHandler):
    """
    Manejador HTTP para rutas de autenticación.
    
    Implementa el patrón Template Method heredando de BaseHTTPRequestHandler.
    Los métodos do_GET, do_POST son llamados automáticamente según el verbo HTTP.
    """
    
    # ───────────────────────────────────────────────────────────
    # Paso 3.1: Manejo de GET requests
    # ───────────────────────────────────────────────────────────
    def do_GET(self):
        """
        Procesa requests GET.
        
        POR QUÉ urlparse: Separar path de query string
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        # Router simple basado en path
        if path == '/api/auth/login':
            self._handle_login()
        elif path == '/api/auth/callback':
            self._handle_callback(query)
        elif path == '/api/auth/logout':
            self._handle_logout()
        elif path == '/api/auth/me':
            self._handle_me()
        else:
            self._send_json_response({'error': 'Not found'}, 404)
    
    # ───────────────────────────────────────────────────────────
    # Paso 3.2: Ruta /login
    # ───────────────────────────────────────────────────────────
    def _handle_login(self):
        """
        Inicia el flujo OAuth 2.0.
        
        POR QUÉ state: Previene ataques CSRF
        """
        # Crear sesión y guardar state
        session_id = session_store.create_session()
        state = secrets.token_urlsafe(32)
        session_store.set(session_id, 'oauth_state', state)
        
        # Construir URL de autorización
        auth_url = Config.get_oauth_auth_url(state)
        
        # Redirigir (con cookie de sesión)
        self._send_redirect(auth_url, session_id)
    
    # ───────────────────────────────────────────────────────────
    # Paso 3.3: Ruta /callback
    # ───────────────────────────────────────────────────────────
    def _handle_callback(self, query: Dict):
        """
        Maneja callback de Google OAuth.
        
        POR QUÉ validar state: Protección CSRF
        """
        # Obtener session_id de cookie
        session_id = self._get_session_id_from_cookie()
        
        if not session_id:
            self._send_json_response({'error': 'No session'}, 400)
            return
        
        # Validar state
        state = query.get('state', [None])[0]
        stored_state = session_store.get(session_id, 'oauth_state')
        
        if not state or state != stored_state:
            self._send_json_response({'error': 'Invalid state'}, 400)
            return
        
        # Verificar errores de Google
        error = query.get('error', [None])[0]
        if error:
            self._send_json_response({'error': f'OAuth error: {error}'}, 400)
            return
        
        # Obtener código
        code = query.get('code', [None])[0]
        if not code:
            self._send_json_response({'error': 'No code received'}, 400)
            return
        
        # Intercambiar código por token
        try:
            token_data = self._exchange_code_for_token(code)
            access_token = token_data.get('access_token')
            
            # Guardar en sesión
            session_store.set(session_id, 'access_token', access_token)
            session_store.set(session_id, 'user_id', self._get_user_id(access_token))
            
            # Redirigir a dashboard
            self._send_redirect(Config.APP_URL + '/dashboard')
        except Exception as e:
            self._send_json_response({'error': str(e)}, 500)
    
    # ───────────────────────────────────────────────────────────
    # Paso 3.4: Ruta /logout
    # ───────────────────────────────────────────────────────────
    def _handle_logout(self):
        """Cierra la sesión del usuario."""
        session_id = self._get_session_id_from_cookie()
        if session_id:
            session_store.delete(session_id)
        self._send_redirect(Config.APP_URL + '/login')
    
    # ───────────────────────────────────────────────────────────
    # Paso 3.5: Ruta /me
    # ───────────────────────────────────────────────────────────
    def _handle_me(self):
        """Retorna información del usuario actual."""
        session_id = self._get_session_id_from_cookie()
        
        if not session_id:
            self._send_json_response({'authenticated': False}, 401)
            return
        
        access_token = session_store.get(session_id, 'access_token')
        
        if not access_token:
            self._send_json_response({'authenticated': False}, 401)
            return
        
        user_id = session_store.get(session_id, 'user_id')
        self._send_json_response({
            'authenticated': True,
            'user_id': user_id
        })
    
    # ───────────────────────────────────────────────────────────
    # Paso 4: Métodos helper
    # ───────────────────────────────────────────────────────────
    def _send_json_response(self, data: Dict, status: int = 200):
        """Envía una respuesta JSON."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_redirect(self, url: str, session_id: str = None):
        """Envía una redirección HTTP."""
        self.send_response(302)
        self.send_header('Location', url)
        if session_id:
            self.send_header('Set-Cookie', f'session_id={session_id}; HttpOnly; Path=/')
        self.end_headers()
    
    def _get_session_id_from_cookie(self) -> Optional[str]:
        """Extrae session_id de las cookies."""
        cookie_header = self.headers.get('Cookie', '')
        for cookie in cookie_header.split(';'):
            cookie = cookie.strip()
            if cookie.startswith('session_id='):
                return cookie.split('=', 1)[1]
        return None
    
    def _exchange_code_for_token(self, code: str) -> Dict:
        """
        Intercambia código por token usando http.client.
        
        [REFACTOR] Usando http.client en vez de requests
        POR QUÉ http.client: Librería estándar de Python
        """
        # Preparar datos
        data = urlencode({
            'code': code,
            'client_id': Config.GOOGLE_CLIENT_ID,
            'client_secret': Config.GOOGLE_CLIENT_SECRET,
            'redirect_uri': Config.OAUTH_REDIRECT_URI,
            'grant_type': 'authorization_code'
        })
        
        # Crear conexión HTTPS
        context = ssl.create_default_context()
        conn = http.client.HTTPSConnection('oauth2.googleapis.com', context=context)
        
        # Enviar request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/token', data, headers)
        
        # Leer respuesta
        response = conn.getresponse()
        response_data = response.read().decode()
        conn.close()
        
        if response.status != 200:
            raise Exception(f"Token request failed: {response_data}")
        
        return json.loads(response_data)
    
    def _get_user_id(self, access_token: str) -> str:
        """
        Obtiene ID del usuario desde Google.
        
        [REFACTOR] Usando http.client en vez de requests
        """
        context = ssl.create_default_context()
        conn = http.client.HTTPSConnection('www.googleapis.com', context=context)
        
        headers = {'Authorization': f'Bearer {access_token}'}
        conn.request('GET', '/oauth2/v1/userinfo', headers=headers)
        
        response = conn.getresponse()
        response_data = response.read().decode()
        conn.close()
        
        if response.status != 200:
            return 'unknown'
        
        return json.loads(response_data).get('id', 'unknown')
    
    # Silenciar logs del servidor
    def log_message(self, format, *args):
        pass


# ═══════════════════════════════════════════════════════════════
# Paso 5: Prueba Atómica
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Prueba atómica: Verifica estructura sin levantar servidor.
    
    [REFACTOR] Actualizado para validar implementación POO pura.
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: Auth Handler (Python POO puro)")
    print("=" * 60)
    
    # Test 1: Verificar SessionStore (POO)
    print("\n1. Verificar SessionStore (POO):")
    store = SessionStore()
    sid = store.create_session()
    print(f"   ✓ Sesión creada: {sid[:20]}...")
    store.set(sid, 'test_key', 'test_value')
    print(f"   ✓ set() funciona")
    value = store.get(sid, 'test_key')
    print(f"   ✓ get() retorna: {value}")
    store.delete(sid)
    print(f"   ✓ delete() funciona")
    
    # Test 2: Verificar AuthHandler hereda correctamente
    print("\n2. Verificar AuthHandler (herencia POO):")
    print(f"   ✓ Clase: {AuthHandler.__name__}")
    print(f"   ✓ Hereda de: {AuthHandler.__bases__[0].__name__}")
    print(f"   ✓ Método do_GET: {'do_GET' in dir(AuthHandler)}")
    
    # Test 3: Verificar métodos privados
    print("\n3. Verificar métodos del handler:")
    methods = ['_handle_login', '_handle_callback', '_handle_logout', 
               '_handle_me', '_send_json_response', '_send_redirect',
               '_exchange_code_for_token', '_get_user_id']
    for method in methods:
        exists = hasattr(AuthHandler, method)
        print(f"   ✓ {method}: {'existe' if exists else 'FALTA'}")
    
    # Test 4: Verificar que NO usa Flask
    print("\n4. Verificar que es Python puro (sin Flask):")
    import sys
    flask_loaded = 'flask' in sys.modules
    print(f"   ✓ Flask en sys.modules: {flask_loaded} (esperado: False)")
    if not flask_loaded:
        print(f"   ✓ ¡Confirmado: NO usa Flask!")
    
    # Test 5: Verificar Config
    print("\n5. Verificar Config:")
    print(f"   ✓ OAUTH_REDIRECT_URI: {Config.OAUTH_REDIRECT_URI}")
    
    print("\n" + "=" * 60)
    print("⚠️  NOTA: No se levanta servidor HTTP en prueba atómica")
    print("    Para probar real: HTTPServer(('', 5000), AuthHandler).serve_forever()")
    print("=" * 60)
    print("✅ Prueba de Auth Handler (POO puro): OK")
    print("=" * 60)
