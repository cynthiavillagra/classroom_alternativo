"""
Vercel Serverless Function Entry Point
Punto único de entrada para Vercel.

[FIX v1.2.5] Corregir manejo de POST para /api/download_zip
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import io

# Agregar raíz al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Cargar .env
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT_DIR, '.env'))
except:
    pass

# Ahora importar desde main
try:
    from main import VercelBridge
    wsgi_app = VercelBridge()
    IMPORT_ERROR = None
except Exception as e:
    wsgi_app = None
    IMPORT_ERROR = str(e)
    import traceback
    IMPORT_TRACEBACK = traceback.format_exc()


class handler(BaseHTTPRequestHandler):
    """Handler HTTP para Vercel Functions."""
    
    def _handle_request(self, method='GET'):
        """Maneja cualquier request HTTP."""
        # Si hubo error al importar, mostrarlo
        if IMPORT_ERROR:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({
                'error': 'Import failed',
                'message': IMPORT_ERROR,
                'traceback': IMPORT_TRACEBACK
            })
            self.wfile.write(error_response.encode())
            return
        
        # Obtener el path real de la request
        raw_path = getattr(self, 'path', '/')
        
        # Construir environ WSGI con COOKIES
        path_info = raw_path.split('?')[0]
        query_string = raw_path.split('?')[1] if '?' in raw_path else ''
        
        # Leer body para POST
        body_input = None
        content_length = 0
        if method == 'POST':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body_data = self.rfile.read(content_length)
                body_input = io.BytesIO(body_data)
        
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'wsgi.input': body_input,
            'CONTENT_LENGTH': str(content_length),
            'CONTENT_TYPE': self.headers.get('Content-Type', ''),
        }
        
        # Agregar headers HTTP (incluyendo cookies!)
        if hasattr(self, 'headers') and self.headers:
            for key, value in self.headers.items():
                wsgi_key = f'HTTP_{key.upper().replace("-", "_")}'
                environ[wsgi_key] = value
        
        # Ejecutar WSGI app
        try:
            response_body = []
            response_status = [200]
            response_headers = []
            
            def start_response(status, headers):
                response_status[0] = int(status.split()[0])
                response_headers.extend(headers)
            
            result = wsgi_app(environ, start_response)
            for data in result:
                response_body.append(data)
            
            # Enviar respuesta
            self.send_response(response_status[0])
            for key, value in response_headers:
                self.send_header(key, value)
            self.end_headers()
            for data in response_body:
                self.wfile.write(data)
                
        except Exception as e:
            import traceback
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({
                'error': 'Runtime error',
                'message': str(e),
                'traceback': traceback.format_exc(),
                'path_info': path_info,
                'method': method
            })
            self.wfile.write(error_response.encode())
    
    def do_GET(self):
        """Maneja GET requests."""
        self._handle_request('GET')
    
    def do_POST(self):
        """Maneja POST requests."""
        self._handle_request('POST')
    
    def log_message(self, format, *args):
        """Silenciar logs."""
        pass
