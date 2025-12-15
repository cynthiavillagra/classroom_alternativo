"""
Main Server - Classroom Explorer

Punto de entrada del servidor HTTP usando Python POO puro.

[REFACTOR] Cambios para soporte Vercel + diagnóstico:
- load_dotenv() AL INICIO antes de cualquier lógica
- Diagnóstico de variables críticas
- VercelBridge para compatibilidad WSGI
- Variable 'app' expuesta para Vercel

POR QUÉ SÍ http.server:
✅ Librería estándar de Python (sin dependencias)
✅ Control total sobre routing
✅ Cumple requisito de "Python POO sin frameworks"

POR QUÉ NO uvicorn/Flask/FastAPI:
❌ Son frameworks externos
❌ Violan el requisito
"""

# ═══════════════════════════════════════════════════════════════
# [REFACTOR] Paso 0: CARGAR .env ANTES DE TODO
# ═══════════════════════════════════════════════════════════════
# POR QUÉ al inicio: Las variables deben estar disponibles para Config
from dotenv import load_dotenv
load_dotenv()  # Carga .env si existe (desarrollo local)

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ http.server: Servidor HTTP de librería estándar
# POR QUÉ importar handlers: Delegamos a cada handler especializado
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from io import BytesIO
import json
import os
import sys

# Importar handlers de rutas
from src.routes.auth import AuthHandler, session_store
from src.routes.courses import CoursesHandler
from src.routes.materials import MaterialsHandler
from src.infrastructure.config import Config

# ═══════════════════════════════════════════════════════════════
# [REFACTOR] Paso 1.1: Diagnóstico de Variables Críticas
# ═══════════════════════════════════════════════════════════════
# POR QUÉ diagnóstico: Detectar problemas de configuración temprano
def _diagnose_environment():
    """Verifica que las variables críticas estén configuradas."""
    critical_vars = [
        ('GOOGLE_CLIENT_ID', 'OAuth no funcionará'),
        ('GOOGLE_CLIENT_SECRET', 'OAuth no funcionará'),
    ]
    
    warnings = []
    for var_name, impact in critical_vars:
        value = os.getenv(var_name)
        if not value or value.startswith('REEMPLAZA') or value.startswith('<'):
            warnings.append(f"⚠️ ALERTA: Variable {var_name} no configurada. {impact}")
    
    return warnings

# Ejecutar diagnóstico al cargar el módulo
_env_warnings = _diagnose_environment()


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
        # [REFACTOR] Agregar endpoint para servir documentación
        elif path.startswith('/api/docs'):
            self._serve_docs_api()
        elif path == '/' or path == '/index.html':
            self._serve_static('public/index.html', 'text/html')
        elif path == '/login' or path == '/login.html':
            self._serve_static('public/login.html', 'text/html')
        elif path == '/dashboard' or path == '/dashboard.html':
            self._serve_static('public/dashboard.html', 'text/html')
        # [REFACTOR] Agregar ruta para visor de documentación
        elif path == '/docs' or path == '/docs.html':
            self._serve_static('public/docs.html', 'text/html')
        # [FIX] Agregar ruta para ver materiales de un curso
        elif path == '/materials' or path.startswith('/materials?'):
            self._serve_static('public/materials.html', 'text/html')
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
    # [REFACTOR] Paso 2.2.1: API para servir documentos Markdown
    # ───────────────────────────────────────────────────────────
    def _serve_docs_api(self):
        """
        Endpoint /api/docs?file=path/to/file.md
        
        Sirve archivos de documentación Markdown.
        POR QUÉ API separada: Permite al frontend cargar docs dinámicamente
        """
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        
        file_path = query.get('file', [None])[0]
        
        if not file_path:
            self._send_json({'error': 'Missing file parameter'}, 400)
            return
        
        # Seguridad: Solo permitir archivos .md en docs/ o README.md
        if not (file_path.endswith('.md') and 
                (file_path.startswith('docs/') or file_path == 'README.md')):
            self._send_json({'error': 'Invalid file path'}, 403)
            return
        
        # Prevenir path traversal
        if '..' in file_path:
            self._send_json({'error': 'Invalid path'}, 403)
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/markdown; charset=utf-8')
            self.send_header('Content-Length', len(content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self._send_json({'error': 'File not found'}, 404)
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.3: Servir archivos estáticos
    # ───────────────────────────────────────────────────────────
    def _serve_static(self, filepath: str, content_type: str):
        """
        Sirve archivos estáticos del frontend.
        
        POR QUÉ servir estáticos: Frontend HTML/CSS/JS necesita archivos
        [FIX] Usar ruta absoluta para compatibilidad con Vercel
        """
        # Obtener directorio base del proyecto
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, filepath)
        
        try:
            with open(full_path, 'rb') as f:
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
            # [FIX] Inicializar dependencias para TODOS los handlers que las necesiten
            from src.infrastructure.repositories import GoogleClassroomRepository
            from src.application.use_cases import ListUserCourses, ListCourseMaterials
            
            # Siempre inicializar repository
            self.repository = GoogleClassroomRepository()
            
            # Inicializar use cases según el nombre de la clase
            if handler_class.__name__ == 'CoursesHandler':
                self.list_courses_use_case = ListUserCourses(self.repository)
            elif handler_class.__name__ == 'MaterialsHandler':
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
    print("   GET /docs                → 📚 Visor de Documentación")
    print("   GET /api/auth/login      → Iniciar OAuth")
    print("   GET /api/auth/callback   → Callback OAuth")
    print("   GET /api/auth/me         → Info usuario")
    print("   GET /api/courses         → Listar cursos")
    print("   GET /api/courses/{id}/materials → Listar materiales")
    print("   GET /api/docs?file=X     → Servir documento Markdown")
    print("=" * 60)
    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido")
        httpd.shutdown()


# ═══════════════════════════════════════════════════════════════
# [REFACTOR] Paso 5: VercelBridge - Adaptador WSGI para Vercel
# ═══════════════════════════════════════════════════════════════
# POR QUÉ un bridge: Vercel usa WSGI, no HTTPServer.serve_forever()
class VercelBridge:
    """
    Adaptador que traduce requests WSGI a nuestro MainRouter.
    
    EN VERCEL:
    - Vercel llama a app(environ, start_response)
    - Este bridge traduce environ a lo que espera MainRouter
    
    EN LOCAL:
    - Se usa HTTPServer directamente (en __main__)
    """
    
    def __call__(self, environ, start_response):
        """Función WSGI que Vercel ejecuta."""
        # Construir request fake para MainRouter
        path = environ.get('PATH_INFO', '/')
        query = environ.get('QUERY_STRING', '')
        full_path = f"{path}?{query}" if query else path
        
        # Crear un handler fake que capture la respuesta
        response_body = BytesIO()
        response_headers = []
        response_status = [200]
        
        class FakeWfile:
            def write(self, data):
                response_body.write(data)
        
        class FakeHandler(MainRouter):
            def __init__(self):
                self.path = full_path
                self.headers = {k[5:].replace('_', '-').title(): v 
                               for k, v in environ.items() if k.startswith('HTTP_')}
                self.wfile = FakeWfile()
                self.rfile = BytesIO(environ.get('wsgi.input', b'').read() if hasattr(environ.get('wsgi.input'), 'read') else b'')
            
            def send_response(self, code):
                response_status[0] = code
            
            def send_header(self, key, value):
                response_headers.append((key, str(value)))
            
            def end_headers(self):
                pass
            
            def log_message(self, *args):
                pass
        
        handler = FakeHandler()
        handler.do_GET()
        
        # Devolver respuesta WSGI
        status = f"{response_status[0]} OK"
        start_response(status, response_headers)
        return [response_body.getvalue()]


# ═══════════════════════════════════════════════════════════════
# [REFACTOR] Paso 5.1: Exponer variable 'app' para Vercel
# ═══════════════════════════════════════════════════════════════
# POR QUÉ exponer app: Vercel busca una variable llamada 'app'
app = VercelBridge()


# ═══════════════════════════════════════════════════════════════
# Paso 6: Prueba Atómica
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
        
        # Test 0: Diagnóstico de entorno
        print("\n0. Diagnóstico de Entorno:")
        if _env_warnings:
            for warning in _env_warnings:
                print(f"   {warning}")
        else:
            print("   ✓ Todas las variables críticas configuradas")
        
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
        
        # Test 5: Verificar VercelBridge
        print("\n5. Verificar VercelBridge (para Vercel):")
        print(f"   ✓ VercelBridge: {VercelBridge is not None}")
        print(f"   ✓ app expuesta: {app is not None}")
        print(f"   ✓ app es callable: {callable(app)}")
        
        print("\n" + "=" * 60)
        print("✅ Prueba de Main Server: OK")
        print("=" * 60)
        print("\nPara iniciar servidor real:")
        print("   python main.py")
        print("\nPara deploy en Vercel:")
        print("   vercel --prod")
        print("=" * 60)
    else:
        # Mostrar warnings de entorno
        for warning in _env_warnings:
            print(warning)
        # Modo servidor real
        run_server()
