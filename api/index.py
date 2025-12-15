"""
Vercel Serverless Function Entry Point
Punto único de entrada para Vercel.
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Agregar raíz al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Cargar .env
from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT_DIR, '.env'))

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
    
    def do_GET(self):
        """Maneja GET requests."""
        # Si hubo error al importar, mostrarlo
        if IMPORT_ERROR:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({
                'error': 'Import failed',
                'message': IMPORT_ERROR,
                'traceback': IMPORT_TRACEBACK,
                'path': sys.path[:5],
                'root_dir': ROOT_DIR
            })
            self.wfile.write(error_response.encode())
            return
        
        # Obtener el path real de la request
        raw_path = getattr(self, 'path', '/')
        
        # Construir environ WSGI
        path_info = raw_path.split('?')[0]
        query_string = raw_path.split('?')[1] if '?' in raw_path else ''
        
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': path_info,
            'QUERY_STRING': query_string,
            'wsgi.input': None,
        }
        
        # Agregar headers HTTP (cookies incluidas)
        if hasattr(self, 'headers') and self.headers:
            for key, value in self.headers.items():
                environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
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
                'raw_path': raw_path
            })
            self.wfile.write(error_response.encode())
    
    def do_POST(self):
        """Maneja POST requests."""
        self.do_GET()
    
    def log_message(self, format, *args):
        """Silenciar logs."""
        pass
