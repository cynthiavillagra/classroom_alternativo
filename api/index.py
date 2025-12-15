"""
Vercel Serverless Function Entry Point

Vercel Python functions deben exportar una función 'handler' 
que reciba (request) y retorne una Response.

ALTERNATIVA: Exportar una variable 'app' que sea WSGI callable.
"""

import sys
import os

# Agregar raíz al path para importar main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar .env si existe (para desarrollo local)
from dotenv import load_dotenv
load_dotenv()

# Importar el VercelBridge de main.py
from main import VercelBridge

# Crear instancia del adaptador WSGI
app = VercelBridge()

# Para Vercel Serverless Functions (HTTP handler)
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    """Handler HTTP para Vercel Functions."""
    
    def do_GET(self):
        """Delega GET al VercelBridge."""
        # Construir environ WSGI
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': self.path.split('?')[0],
            'QUERY_STRING': self.path.split('?')[1] if '?' in self.path else '',
            'wsgi.input': None,
        }
        
        # Agregar headers HTTP
        for key, value in self.headers.items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        # Capturar respuesta
        response_started = [False]
        response_headers = []
        
        def start_response(status, headers):
            response_started[0] = True
            self.send_response(int(status.split()[0]))
            for key, value in headers:
                self.send_header(key, value)
            self.end_headers()
        
        # Ejecutar WSGI app
        result = app(environ, start_response)
        
        # Escribir body
        for data in result:
            self.wfile.write(data)
    
    def do_POST(self):
        """Delega POST al VercelBridge."""
        self.do_GET()  # Por ahora, mismo handling
