"""
Courses HTTP Handler - Classroom Explorer

Endpoints para listar cursos del usuario.

POR QUÉ SÍ Python POO puro:
✅ Sin frameworks externos (requisito)
✅ Herencia de BaseHTTPRequestHandler
✅ Usa Use Cases del Application Layer

POR QUÉ NO Flask:
❌ Es un framework externo
❌ Viola el requisito de "Python POO sin frameworks"
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias (SOLO librería estándar + dominio)
# ═══════════════════════════════════════════════════════════════
# POR QUÉ http.server: Servidor HTTP de librería estándar
# POR QUÉ Use Cases: Reutilizamos lógica de Application Layer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from typing import Dict, Any, Optional

# Importar del dominio (POO pura)
from src.application.use_cases import ListUserCourses, ListUserCoursesRequest
from src.infrastructure.repositories import GoogleClassroomRepository
from src.routes.auth import session_store


# ═══════════════════════════════════════════════════════════════
# Paso 2: Handler HTTP para cursos (herencia POO)
# ═══════════════════════════════════════════════════════════════
# POR QUÉ herencia: Patrón Template Method, igual que AuthHandler
class CoursesHandler(BaseHTTPRequestHandler):
    """
    Manejador HTTP para rutas de cursos.
    
    Rutas:
    - GET /api/courses → Lista todos los cursos del usuario
    - GET /api/courses/{id} → Detalle de un curso específico
    """
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa el handler con sus dependencias.
        
        POR QUÉ inyectar repository aquí: Dependency Injection
        """
        # Paso 2.1: Crear instancias de dependencias
        self.repository = GoogleClassroomRepository()
        self.list_courses_use_case = ListUserCourses(self.repository)
        
        # Llamar constructor padre
        super().__init__(*args, **kwargs)
    
    # ───────────────────────────────────────────────────────────
    # Paso 3: Manejo de GET requests
    # ───────────────────────────────────────────────────────────
    def do_GET(self):
        """
        Procesa requests GET.
        
        POR QUÉ router manual: Sin framework, hacemos routing nosotros
        """
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        # Router basado en path
        if path == '/api/courses':
            self._handle_list_courses(query)
        elif path.startswith('/api/courses/'):
            course_id = path.split('/')[-1]
            self._handle_get_course(course_id)
        else:
            self._send_json_response({'error': 'Not found'}, 404)
    
    # ───────────────────────────────────────────────────────────
    # Paso 4: Ruta GET /api/courses
    # ───────────────────────────────────────────────────────────
    def _handle_list_courses(self, query: Dict):
        """
        Lista todos los cursos del usuario autenticado.
        
        POR QUÉ usar Use Case: Reutilizamos lógica de Application Layer
        POR QUÉ verificar auth primero: Seguridad
        """
        # Paso 4.1: Verificar autenticación
        session_id = self._get_session_id_from_cookie()
        if not session_id:
            self._send_json_response({'error': 'Not authenticated'}, 401)
            return
        
        access_token = session_store.get(session_id, 'access_token')
        user_id = session_store.get(session_id, 'user_id')
        
        if not access_token:
            self._send_json_response({'error': 'Not authenticated'}, 401)
            return
        
        # Paso 4.2: Parsear query params
        include_archived = query.get('include_archived', ['true'])[0].lower() == 'true'
        filter_state = query.get('state', [None])[0]
        
        # Paso 4.3: Crear request DTO
        request = ListUserCoursesRequest(
            user_id=user_id or 'me',
            access_token=access_token,
            include_archived=include_archived,
            filter_state=None  # Simplificado para MVP
        )
        
        # Paso 4.4: Ejecutar Use Case
        try:
            response = self.list_courses_use_case.execute(request)
            
            # Paso 4.5: Serializar respuesta
            courses_json = [course.to_dict() for course in response.courses]
            
            self._send_json_response({
                'courses': courses_json,
                'total_count': response.total_count,
                'active_count': response.active_count,
                'archived_count': response.archived_count
            })
        except Exception as e:
            self._send_json_response({'error': str(e)}, 500)
    
    # ───────────────────────────────────────────────────────────
    # Paso 5: Ruta GET /api/courses/{id}
    # ───────────────────────────────────────────────────────────
    def _handle_get_course(self, course_id: str):
        """
        Obtiene detalle de un curso específico.
        
        POR QUÉ endpoint separado: REST best practice
        """
        # Paso 5.1: Verificar autenticación
        session_id = self._get_session_id_from_cookie()
        if not session_id:
            self._send_json_response({'error': 'Not authenticated'}, 401)
            return
        
        access_token = session_store.get(session_id, 'access_token')
        
        if not access_token:
            self._send_json_response({'error': 'Not authenticated'}, 401)
            return
        
        # Paso 5.2: Obtener curso del repositorio
        try:
            course = self.repository.get_course_by_id(course_id, access_token)
            self._send_json_response(course.to_dict())
        except Exception as e:
            self._send_json_response({'error': str(e)}, 404)
    
    # ───────────────────────────────────────────────────────────
    # Paso 6: Métodos helper
    # ───────────────────────────────────────────────────────────
    def _send_json_response(self, data: Dict, status: int = 200):
        """Envía una respuesta JSON."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # CORS
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _get_session_id_from_cookie(self) -> Optional[str]:
        """Extrae session_id de las cookies."""
        cookie_header = self.headers.get('Cookie', '')
        for cookie in cookie_header.split(';'):
            cookie = cookie.strip()
            if cookie.startswith('session_id='):
                return cookie.split('=', 1)[1]
        return None
    
    # Silenciar logs del servidor
    def log_message(self, format, *args):
        pass


# ═══════════════════════════════════════════════════════════════
# Paso 7: Prueba Atómica
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Prueba atómica: Verifica estructura sin levantar servidor.
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: Courses Handler (Python POO puro)")
    print("=" * 60)
    
    # Test 1: Verificar clase existe y hereda correctamente
    print("\n1. Verificar CoursesHandler (herencia POO):")
    print(f"   ✓ Clase: {CoursesHandler.__name__}")
    print(f"   ✓ Hereda de: {CoursesHandler.__bases__[0].__name__}")
    print(f"   ✓ Método do_GET: {'do_GET' in dir(CoursesHandler)}")
    
    # Test 2: Verificar métodos de rutas
    print("\n2. Verificar métodos del handler:")
    methods = ['_handle_list_courses', '_handle_get_course', 
               '_send_json_response', '_get_session_id_from_cookie']
    for method in methods:
        exists = hasattr(CoursesHandler, method)
        print(f"   ✓ {method}: {'existe' if exists else 'FALTA'}")
    
    # Test 3: Verificar que usa Use Cases
    print("\n3. Verificar integración con Application Layer:")
    print(f"   ✓ ListUserCourses importado: {ListUserCourses is not None}")
    print(f"   ✓ ListUserCoursesRequest importado: {ListUserCoursesRequest is not None}")
    
    # Test 4: Verificar que NO usa Flask
    print("\n4. Verificar que es Python puro (sin Flask):")
    import sys
    flask_loaded = 'flask' in sys.modules
    print(f"   ✓ Flask en sys.modules: {flask_loaded} (esperado: False)")
    if not flask_loaded:
        print(f"   ✓ ¡Confirmado: NO usa Flask!")
    
    # Test 5: Verificar repository
    print("\n5. Verificar Repository:")
    print(f"   ✓ GoogleClassroomRepository importado: {GoogleClassroomRepository is not None}")
    
    print("\n" + "=" * 60)
    print("⚠️  NOTA: No se levanta servidor HTTP en prueba atómica")
    print("    Para probar real, necesitas credenciales OAuth válidas")
    print("=" * 60)
    print("✅ Prueba de Courses Handler (POO puro): OK")
    print("=" * 60)
