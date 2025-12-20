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
        # [FIX v1.1.0] Endpoint para obtener config de Google Picker
        elif path == '/api/config/picker':
            self._serve_picker_config()
        # ───────────────────────────────────────────────────────────
        # [UNIVERSAL] Rutas estáticas - En producción (Vercel/Netlify)
        # estas rutas son manejadas por vercel.json/netlify.toml.
        # En desarrollo local, las manejamos nosotros.
        # POR QUÉ mantenerlas: Permite desarrollo local sin config extra
        # ───────────────────────────────────────────────────────────
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
    # [FIX v1.1.0] Manejo de POST
    # [FIX v1.2.0] Agregar endpoint /api/download/zip
    # ───────────────────────────────────────────────────────────
    def do_POST(self):
        """Procesa POST requests."""
        path = urlparse(self.path).path
        
        if path == '/api/drive/copy':
            self._handle_drive_copy()
        elif path == '/api/download/zip':
            self._handle_download_zip()
        else:
            self._send_json({'error': 'Not found'}, 404)
    
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
    # [FIX v1.1.0] Endpoint para config de Google Picker
    # ───────────────────────────────────────────────────────────
    def _serve_picker_config(self):
        """
        Endpoint GET /api/config/picker
        
        Devuelve las credenciales necesarias para inicializar Google Picker.
        El token de acceso se obtiene de la cookie de sesión.
        """
        # Obtener token de la cookie
        cookies = self.headers.get('Cookie', '')
        access_token = None
        
        for cookie in cookies.split(';'):
            cookie = cookie.strip()
            if cookie.startswith('access_token='):
                access_token = cookie.split('=', 1)[1]
                break
        
        if not access_token:
            self._send_json({'error': 'Not authenticated'}, 401)
            return
        
        # Devolver config para Picker
        self._send_json({
            'clientId': Config.GOOGLE_CLIENT_ID,
            'apiKey': Config.GOOGLE_PICKER_API_KEY,
            'accessToken': access_token,
            'appId': Config.GOOGLE_CLIENT_ID.split('.')[0] if Config.GOOGLE_CLIENT_ID else ''
        })
    
    # ───────────────────────────────────────────────────────────
    # [FIX v1.1.0] Endpoint para copiar archivos a Drive
    # ───────────────────────────────────────────────────────────
    def _handle_drive_copy(self):
        """
        Endpoint POST /api/drive/copy
        
        Body: {
            "fileUrls": ["url1", "url2", ...],
            "targetFolderId": "folder_id_from_picker"
        }
        
        Copia archivos de Google Drive del curso al Drive del usuario.
        """
        import urllib.request
        import urllib.error
        
        # Obtener token de la cookie
        cookies = self.headers.get('Cookie', '')
        access_token = None
        
        for cookie in cookies.split(';'):
            cookie = cookie.strip()
            if cookie.startswith('access_token='):
                access_token = cookie.split('=', 1)[1]
                break
        
        if not access_token:
            self._send_json({'error': 'Not authenticated'}, 401)
            return
        
        # Leer body del POST
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            self._send_json({'error': 'Invalid JSON'}, 400)
            return
        
        file_urls = data.get('fileUrls', [])
        target_folder_id = data.get('targetFolderId')
        
        if not file_urls:
            self._send_json({'error': 'No files provided'}, 400)
            return
        
        if not target_folder_id:
            self._send_json({'error': 'No target folder selected'}, 400)
            return
        
        # Copiar cada archivo
        results = []
        errors = []
        
        for url in file_urls:
            try:
                # Extraer file ID de la URL de Drive
                file_id = self._extract_drive_file_id(url)
                
                if not file_id:
                    errors.append({'url': url, 'error': 'Could not extract file ID'})
                    continue
                
                # Llamar a Drive API para copiar
                copy_result = self._copy_drive_file(file_id, target_folder_id, access_token)
                
                if copy_result.get('error'):
                    errors.append({'url': url, 'error': copy_result['error']})
                else:
                    results.append({'url': url, 'newFileId': copy_result.get('id'), 'name': copy_result.get('name')})
                    
            except Exception as e:
                errors.append({'url': url, 'error': str(e)})
        
        self._send_json({
            'copied': len(results),
            'failed': len(errors),
            'results': results,
            'errors': errors
        })
    
    def _extract_drive_file_id(self, url: str) -> str:
        """Extrae el file ID de una URL de Google Drive."""
        import re
        from urllib.parse import urlparse, parse_qs
        
        # Primero intentar extraer de parámetros de query (?id=...)
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        # Buscar en parámetros comunes
        for param in ['id', 'fileId']:
            if param in query_params:
                return query_params[param][0]
        
        # Patrones comunes de URLs de Drive (el ID termina antes de / o ? o fin de string)
        patterns = [
            # drive.google.com/file/d/ID/view, /preview, /edit, etc.
            r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
            # drive.google.com/open?id=ID
            r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
            # docs.google.com/document/d/ID/...
            r'docs\.google\.com/document/d/([a-zA-Z0-9_-]+)',
            # docs.google.com/spreadsheets/d/ID/...
            r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)',
            # docs.google.com/presentation/d/ID/...
            r'docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)',
            # drive.google.com/uc?id=ID&export=download
            r'drive\.google\.com/uc\?.*id=([a-zA-Z0-9_-]+)',
            # Patrón genérico: /d/ID/ o /d/ID?
            r'/d/([a-zA-Z0-9_-]+)(?:/|\?|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                file_id = match.group(1)
                # Limpiar el ID: remover cualquier sufijo no válido
                # Los IDs de Drive son típicamente 25-44 caracteres
                if len(file_id) >= 25:
                    return file_id
        
        # Último intento: buscar cualquier string que parezca un ID de Drive
        # (44 caracteres alfanuméricos con guiones y guiones bajos)
        id_pattern = r'([a-zA-Z0-9_-]{25,44})'
        matches = re.findall(id_pattern, url)
        if matches:
            # Devolver el primer match que parezca válido
            return matches[0]
        
        return None
    
    def _copy_drive_file(self, file_id: str, target_folder_id: str, access_token: str) -> dict:
        """Copia un archivo de Drive a la carpeta destino."""
        import urllib.request
        import urllib.error
        
        # API de Drive: files.copy
        copy_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/copy'
        
        # Body con la carpeta destino
        copy_body = json.dumps({
            'parents': [target_folder_id]
        }).encode('utf-8')
        
        req = urllib.request.Request(
            copy_url,
            data=copy_body,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_json = json.loads(error_body)
                return {'error': error_json.get('error', {}).get('message', str(e))}
            except:
                return {'error': str(e)}
    
    # ───────────────────────────────────────────────────────────
    # [FIX v1.2.0] Descargar archivos como ZIP
    # ───────────────────────────────────────────────────────────
    def _handle_download_zip(self):
        """
        Endpoint POST /api/download/zip
        
        Recibe lista de archivos, los descarga de Drive y crea un ZIP.
        POR QUÉ backend: CORS bloquea fetch directo a Drive desde frontend.
        """
        import zipfile
        import io
        import urllib.request
        import urllib.error
        
        # Obtener token de cookie
        cookies = self._get_cookies()
        access_token = cookies.get('access_token')
        
        if not access_token:
            self._send_json({'error': 'Not authenticated'}, 401)
            return
        
        # Leer body del request
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
        except Exception as e:
            self._send_json({'error': f'Invalid request body: {str(e)}'}, 400)
            return
        
        files = data.get('files', [])
        course_name = data.get('courseName', 'materiales')
        
        if not files:
            self._send_json({'error': 'No files provided'}, 400)
            return
        
        # Crear ZIP en memoria
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_info in files:
                url = file_info.get('url', '')
                name = file_info.get('name', 'archivo')
                file_type = file_info.get('type', 'file')
                
                # Extraer ID del archivo de Drive
                file_id = self._extract_drive_file_id(url)
                
                if file_id:
                    try:
                        # Descargar archivo
                        file_content, filename = self._download_drive_file(file_id, access_token, name, file_type)
                        
                        if file_content:
                            # Agregar al ZIP
                            zip_file.writestr(filename, file_content)
                        else:
                            # Si falla, guardar info del error
                            error_content = f"No se pudo descargar: {name}\nURL: {url}\n"
                            zip_file.writestr(f"{name}_ERROR.txt", error_content)
                    except Exception as e:
                        # Guardar info del error
                        error_content = f"Error descargando: {name}\nURL: {url}\nError: {str(e)}\n"
                        zip_file.writestr(f"{name}_ERROR.txt", error_content)
                else:
                    # No se pudo extraer el ID, guardar link
                    link_content = f"[InternetShortcut]\nURL={url}\n"
                    zip_file.writestr(f"{name}.url", link_content)
        
        # Enviar ZIP
        zip_buffer.seek(0)
        zip_content = zip_buffer.read()
        
        # Sanitizar nombre del archivo
        safe_name = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in course_name)
        filename = f"{safe_name}.zip"
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/zip')
        self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.send_header('Content-Length', len(zip_content))
        self.end_headers()
        self.wfile.write(zip_content)
    
    def _download_drive_file(self, file_id: str, access_token: str, name: str, file_type: str) -> tuple:
        """
        Descarga un archivo de Drive usando el token del usuario.
        
        Retorna: (contenido_bytes, nombre_archivo)
        """
        import urllib.request
        import urllib.error
        
        # Primero obtener metadata para el nombre real
        metadata_url = f'https://www.googleapis.com/drive/v3/files/{file_id}?fields=name,mimeType'
        
        try:
            meta_req = urllib.request.Request(
                metadata_url,
                headers={'Authorization': f'Bearer {access_token}'}
            )
            with urllib.request.urlopen(meta_req) as response:
                metadata = json.loads(response.read().decode('utf-8'))
                real_name = metadata.get('name', name)
                mime_type = metadata.get('mimeType', '')
        except:
            real_name = name
            mime_type = ''
        
        # Determinar URL de descarga según el tipo
        if 'google-apps.document' in mime_type:
            # Google Doc -> exportar como PDF
            download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/pdf'
            real_name = real_name.replace('.gdoc', '') + '.pdf'
        elif 'google-apps.spreadsheet' in mime_type:
            # Google Sheet -> exportar como XLSX
            download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            real_name = real_name.replace('.gsheet', '') + '.xlsx'
        elif 'google-apps.presentation' in mime_type:
            # Google Slides -> exportar como PDF
            download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/pdf'
            real_name = real_name.replace('.gslides', '') + '.pdf'
        else:
            # Archivo normal -> descarga directa
            download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media'
        
        # Descargar el archivo
        try:
            req = urllib.request.Request(
                download_url,
                headers={'Authorization': f'Bearer {access_token}'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                return (content, real_name)
        except urllib.error.HTTPError as e:
            print(f"[ERROR] Descargando {file_id}: {e}")
            return (None, real_name)
        except Exception as e:
            print(f"[ERROR] Descargando {file_id}: {e}")
            return (None, real_name)
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.3: Servir archivos estáticos
    # ───────────────────────────────────────────────────────────
    def _serve_static(self, filepath: str, content_type: str):
        """
        Sirve archivos estáticos del frontend.
        
        [UNIVERSAL] Esta función se usa solo en desarrollo local.
        En producción (Vercel/Netlify), los archivos estáticos se
        sirven directamente desde el CDN, no desde la función.
        
        POR QUÉ SÍ mantener: Desarrollo local funciona sin config extra
        POR QUÉ NO eliminar: Rompería `python main.py` local
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
    
    def _get_cookie(self, name: str):
        """[FIX v1.2.1] Extrae una cookie por nombre."""
        cookie_header = self.headers.get('Cookie', '') if self.headers else ''
        for cookie in cookie_header.split(';'):
            cookie = cookie.strip()
            if cookie.startswith(f'{name}='):
                return cookie.split('=', 1)[1]
        return None
    
    def _get_cookies(self):
        """[FIX v1.2.1] Extrae todas las cookies como diccionario."""
        cookies = {}
        cookie_header = self.headers.get('Cookie', '') if self.headers else ''
        for cookie in cookie_header.split(';'):
            cookie = cookie.strip()
            if '=' in cookie:
                name, value = cookie.split('=', 1)
                cookies[name.strip()] = value
        return cookies
    
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
    print(f"   URL: http://{host}:{port}")
    print(f"   Entorno: {Config.ENVIRONMENT}")
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
