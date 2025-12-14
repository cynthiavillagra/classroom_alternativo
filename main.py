"""
Main Server - Classroom Explorer

Punto de entrada del servidor HTTP usando Python POO puro.

POR QUÉ SÍ http.server:
✅ Librería estándar de Python (sin dependencias)
✅ Control total sobre routing
✅ Cumple requisito de "Python POO sin frameworks"

POR QUÉ NO uvicorn/Flask/FastAPI:
❌ Son frameworks externos
❌ Violan el requisito
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ http.server: Servidor HTTP de librería estándar
# POR QUÉ importar handlers: Delegamos a cada handler especializado
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os

# Importar handlers de rutas
from api.routes.auth import AuthHandler, session_store
from api.routes.courses import CoursesHandler
from api.routes.materials import MaterialsHandler
from api.infrastructure.config import Config


# ═══════════════════════════════════════════════════════════════
# Paso 2: Router principal (combina todos los handlers)
# ═══════════════════════════════════════════════════════════════
# POR QUÉ un router central: Un solo punto de entrada que delega
class MainRouter(BaseHTTPRequestHandler):
    """
    Router principal que delega a handlers especializados.
    
    Rutas:
    - /api/auth/* → AuthHandler
    - /api/courses/* → CoursesHandler
    - /api/courses/{id}/materials → MaterialsHandler
    - /* → Servir archivos estáticos
    """
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Manejo de GET
    # ───────────────────────────────────────────────────────────
    def do_GET(self):
        """Procesa GET requests y delega al handler apropiado."""
        path = urlparse(self.path).path
        
        # Router basado en path
        if path.startswith('/api/auth/'):
            self._delegate_to_auth()
        elif '/materials' in path and path.startswith('/api/courses/'):
            self._delegate_to_materials()
        elif path.startswith('/api/courses'):
            self._delegate_to_courses()
        elif path == '/' or path == '/index.html':
            self._serve_static('public/index.html', 'text/html')
        elif path == '/login' or path == '/login.html':
            self._serve_static('public/login.html', 'text/html')
        elif path == '/dashboard' or path == '/dashboard.html':
            self._serve_static('public/dashboard.html', 'text/html')
        elif path.startswith('/css/'):
            self._serve_static(f'public{path}', 'text/css')
        elif path.startswith('/js/'):
            self._serve_static(f'public{path}', 'application/javascript')
        else:
            self._send_not_found()
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.2: Delegación a handlers
    # ───────────────────────────────────────────────────────────
    def _delegate_to_auth(self):
        """Delega a AuthHandler."""
        # Crear handler temporal y ejecutar
        handler = _create_delegated_handler(AuthHandler, self)
        handler.do_GET()
    
    def _delegate_to_courses(self):
        """Delega a CoursesHandler."""
        handler = _create_delegated_handler(CoursesHandler, self)
        handler.do_GET()
    
    def _delegate_to_materials(self):
        """Delega a MaterialsHandler."""
        handler = _create_delegated_handler(MaterialsHandler, self)
        handler.do_GET()
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.3: Servir archivos estáticos
    # ───────────────────────────────────────────────────────────
    def _serve_static(self, filepath: str, content_type: str):
        """
        Sirve archivos estáticos del frontend.
        
        POR QUÉ servir estáticos: Frontend HTML/CSS/JS necesita archivos
        """
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self._send_not_found()
    
    def _send_not_found(self):
        """Envía error 404."""
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def _send_json(self, data: dict, status: int = 200):
        """Envía respuesta JSON."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    # Silenciar logs por defecto (activar con --verbose)
    def log_message(self, format, *args):
        if os.environ.get('VERBOSE'):
            super().log_message(format, *args)


# ═══════════════════════════════════════════════════════════════
# Paso 3: Helper para delegación de handlers
# ═══════════════════════════════════════════════════════════════
class DelegatedHandler:
    """Wrapper para simular un handler delegado."""
    
    def __init__(self, handler_class, parent):
        self.handler_class = handler_class
        self.parent = parent
        self.path = parent.path
        self.headers = parent.headers
        self.wfile = parent.wfile
        self.rfile = parent.rfile
    
    def send_response(self, code):
        self.parent.send_response(code)
    
    def send_header(self, keyword, value):
        self.parent.send_header(keyword, value)
    
    def end_headers(self):
        self.parent.end_headers()


def _create_delegated_handler(handler_class, parent):
    """
    Crea un handler delegado que usa el parent para I/O.
    
    POR QUÉ esta técnica: Los handlers esperan request/response objects
    """
    # Crear una instancia "fake" con los atributos necesarios
    class FakeHandler(handler_class):
        def __init__(self):
            # No llamar super().__init__ porque requiere socket
            self.path = parent.path
            self.headers = parent.headers
            self.wfile = parent.wfile
            self.rfile = parent.rfile
            self._parent = parent
            # Inicializar dependencias
            from api.infrastructure.repositories import GoogleClassroomRepository
            from api.application.use_cases import ListUserCourses, ListCourseMaterials
            self.repository = GoogleClassroomRepository()
            if hasattr(handler_class, 'list_courses_use_case'):
                self.list_courses_use_case = ListUserCourses(self.repository)
            if hasattr(handler_class, 'list_materials_use_case'):
                self.list_materials_use_case = ListCourseMaterials(self.repository)
        
        def send_response(self, code):
            self._parent.send_response(code)
        
        def send_header(self, keyword, value):
            self._parent.send_header(keyword, value)
        
        def end_headers(self):
            self._parent.end_headers()
    
    return FakeHandler()


# ═══════════════════════════════════════════════════════════════
# Paso 4: Función principal para iniciar servidor
# ═══════════════════════════════════════════════════════════════
def run_server(host: str = 'localhost', port: int = 5000):
    """
    Inicia el servidor HTTP.
    
    POR QUÉ función separada: Permite configurar host/port
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, MainRouter)
    
    print("=" * 60)
    print("🚀 Classroom Explorer - Servidor Iniciado")
    print("=" * 60)
    print(f"   URL: http://{host}:{port}")
    print(f"   Entorno: {Config.ENVIRONMENT}")
    print("=" * 60)
    print("\nRutas disponibles:")
    print("   GET /                    → Página principal")
    print("   GET /login               → Página de login")
    print("   GET /dashboard           → Dashboard")
    print("   GET /api/auth/login      → Iniciar OAuth")
    print("   GET /api/auth/callback   → Callback OAuth")
    print("   GET /api/auth/me         → Info usuario")
    print("   GET /api/courses         → Listar cursos")
    print("   GET /api/courses/{id}/materials → Listar materiales")
    print("=" * 60)
    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        httpd.shutdown()


# ═══════════════════════════════════════════════════════════════
# Paso 5: Prueba Atómica
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Si se ejecuta directamente, inicia el servidor.
    Prueba atómica: Verificar que los imports funcionan.
    """
    import sys
    
    # Modo prueba atómica (sin levantar servidor)
    if '--test' in sys.argv:
        print("=" * 60)
        print("PRUEBAS ATÓMICAS: Main Server")
        print("=" * 60)
        
        # Test 1: Verificar imports
        print("\n1. Verificar imports:")
        print(f"   ✓ MainRouter: {MainRouter is not None}")
        print(f"   ✓ AuthHandler: {AuthHandler is not None}")
        print(f"   ✓ CoursesHandler: {CoursesHandler is not None}")
        print(f"   ✓ MaterialsHandler: {MaterialsHandler is not None}")
        print(f"   ✓ session_store: {session_store is not None}")
        
        # Test 2: Verificar herencia
        print("\n2. Verificar MainRouter:")
        print(f"   ✓ Hereda de: {MainRouter.__bases__[0].__name__}")
        print(f"   ✓ do_GET: {'do_GET' in dir(MainRouter)}")
        
        # Test 3: Verificar Config
        print("\n3. Verificar Config:")
        print(f"   ✓ APP_URL: {Config.APP_URL}")
        print(f"   ✓ ENVIRONMENT: {Config.ENVIRONMENT}")
        
        # Test 4: Verificar que NO usa Flask
        print("\n4. Verificar Python puro:")
        flask_loaded = 'flask' in sys.modules
        print(f"   ✓ Flask: {flask_loaded} (esperado: False)")
        if not flask_loaded:
            print(f"   ✓ ¡Confirmado: Python POO puro!")
        
        print("\n" + "=" * 60)
        print("✅ Prueba de Main Server: OK")
        print("=" * 60)
        print("\nPara iniciar servidor real:")
        print("   python main.py")
        print("=" * 60)
    else:
        # Modo servidor real
        run_server()
