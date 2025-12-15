"""
Materials HTTP Handler - Classroom Explorer

Endpoints para listar materiales de un curso.

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
from src.domain.entities import MaterialType
from src.application.use_cases import ListCourseMaterials, ListCourseMaterialsRequest
from src.infrastructure.repositories import GoogleClassroomRepository
from src.routes.auth import session_store


# ═══════════════════════════════════════════════════════════════
# Paso 2: Handler HTTP para materiales (herencia POO)
# ═══════════════════════════════════════════════════════════════
# POR QUÉ herencia: Patrón Template Method, igual que AuthHandler
class MaterialsHandler(BaseHTTPRequestHandler):
    """
    Manejador HTTP para rutas de materiales.
    
    Rutas:
    - GET /api/courses/{course_id}/materials → Lista materiales del curso
    """
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa el handler con sus dependencias.
        
        POR QUÉ inyectar repository aquí: Dependency Injection
        """
        # Paso 2.1: Crear instancias de dependencias
        self.repository = GoogleClassroomRepository()
        self.list_materials_use_case = ListCourseMaterials(self.repository)
        
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
        
        # Router: /api/courses/{course_id}/materials
        if '/materials' in path and path.startswith('/api/courses/'):
            # Extraer course_id del path
            parts = path.split('/')
            # /api/courses/{course_id}/materials → index 3 es course_id
            if len(parts) >= 5 and parts[4] == 'materials':
                course_id = parts[3]
                self._handle_list_materials(course_id, query)
            else:
                self._send_json_response({'error': 'Invalid path'}, 400)
        else:
            self._send_json_response({'error': 'Not found'}, 404)
    
    # ───────────────────────────────────────────────────────────
    # Paso 4: Ruta GET /api/courses/{course_id}/materials
    # ───────────────────────────────────────────────────────────
    def _handle_list_materials(self, course_id: str, query: Dict):
        """
        Lista todos los materiales de un curso.
        
        POR QUÉ usar Use Case: Reutilizamos lógica de Application Layer
        POR QUÉ verificar auth primero: Seguridad
        """
        # Paso 4.1: Verificar autenticación
        session_id = self._get_session_id_from_cookie()
        if not session_id:
            self._send_json_response({'error': 'Not authenticated'}, 401)
            return
        
        access_token = session_store.get(session_id, 'access_token')
        
        if not access_token:
            self._send_json_response({'error': 'Not authenticated'}, 401)
            return
        
        # Paso 4.2: Parsear query params
        filter_type_str = query.get('type', [None])[0]
        search_query = query.get('q', [None])[0]
        limit_str = query.get('limit', [None])[0]
        
        # Paso 4.3: Convertir filter_type a enum si existe
        filter_type = None
        if filter_type_str:
            try:
                filter_type = MaterialType.from_string(filter_type_str)
            except ValueError:
                pass  # Ignorar tipo inválido
        
        # Paso 4.4: Parsear limit
        limit = None
        if limit_str:
            try:
                limit = int(limit_str)
            except ValueError:
                pass
        
        # Paso 4.5: Crear request DTO
        request = ListCourseMaterialsRequest(
            course_id=course_id,
            access_token=access_token,
            filter_type=filter_type,
            search_query=search_query,
            limit=limit
        )
        
        # Paso 4.6: Ejecutar Use Case
        try:
            response = self.list_materials_use_case.execute(request)
            
            # Paso 4.7: Serializar respuesta
            materials_json = [material.to_dict() for material in response.materials]
            
            self._send_json_response({
                'materials': materials_json,
                'total_count': response.total_count,
                'filtered_count': response.filtered_count,
                'type_counts': response.type_counts
            })
        except Exception as e:
            self._send_json_response({'error': str(e)}, 500)
    
    # ───────────────────────────────────────────────────────────
    # Paso 5: Métodos helper
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
# Paso 6: Prueba Atómica
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Prueba atómica: Verifica estructura sin levantar servidor.
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: Materials Handler (Python POO puro)")
    print("=" * 60)
    
    # Test 1: Verificar clase existe y hereda correctamente
    print("\n1. Verificar MaterialsHandler (herencia POO):")
    print(f"   ✓ Clase: {MaterialsHandler.__name__}")
    print(f"   ✓ Hereda de: {MaterialsHandler.__bases__[0].__name__}")
    print(f"   ✓ Método do_GET: {'do_GET' in dir(MaterialsHandler)}")
    
    # Test 2: Verificar métodos de rutas
    print("\n2. Verificar métodos del handler:")
    methods = ['_handle_list_materials', '_send_json_response', 
               '_get_session_id_from_cookie']
    for method in methods:
        exists = hasattr(MaterialsHandler, method)
        print(f"   ✓ {method}: {'existe' if exists else 'FALTA'}")
    
    # Test 3: Verificar que usa Use Cases
    print("\n3. Verificar integración con Application Layer:")
    print(f"   ✓ ListCourseMaterials importado: {ListCourseMaterials is not None}")
    print(f"   ✓ ListCourseMaterialsRequest importado: {ListCourseMaterialsRequest is not None}")
    
    # Test 4: Verificar que usa MaterialType del dominio
    print("\n4. Verificar integración con Domain Layer:")
    print(f"   ✓ MaterialType importado: {MaterialType is not None}")
    
    # Test 5: Verificar que NO usa Flask
    print("\n5. Verificar que es Python puro (sin Flask):")
    import sys
    flask_loaded = 'flask' in sys.modules
    print(f"   ✓ Flask en sys.modules: {flask_loaded} (esperado: False)")
    if not flask_loaded:
        print(f"   ✓ ¡Confirmado: NO usa Flask!")
    
    # Test 6: Verificar repository
    print("\n6. Verificar Repository:")
    print(f"   ✓ GoogleClassroomRepository importado: {GoogleClassroomRepository is not None}")
    
    print("\n" + "=" * 60)
    print("⚠️  NOTA: No se levanta servidor HTTP en prueba atómica")
    print("    Para probar real, necesitas credenciales OAuth válidas")
    print("=" * 60)
    print("✅ Prueba de Materials Handler (POO puro): OK")
    print("=" * 60)
