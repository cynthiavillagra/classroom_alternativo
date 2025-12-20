"""
Vercel Serverless Function: Download ZIP
Endpoint POST /api/download_zip

[FIX v1.2.3] Archivo en raíz de api/ para compatibilidad con Vercel.
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import zipfile
import io
import urllib.request
import urllib.error
import re

# Agregar raíz al path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Cargar .env
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT_DIR, '.env'))
except:
    pass


class handler(BaseHTTPRequestHandler):
    """Handler para descargar archivos como ZIP."""
    
    def do_POST(self):
        """Maneja POST /api/download_zip."""
        try:
            # Obtener token de cookie
            access_token = self._get_cookie('access_token')
            
            if not access_token:
                self._send_json({'error': 'Not authenticated'}, 401)
                return
            
            # Leer body del request
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
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
                            file_content, filename = self._download_drive_file(file_id, access_token, name)
                            
                            if file_content:
                                zip_file.writestr(filename, file_content)
                            else:
                                error_content = f"No se pudo descargar: {name}\nURL: {url}\n"
                                zip_file.writestr(f"{name}_ERROR.txt", error_content)
                        except Exception as e:
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
            
        except Exception as e:
            import traceback
            self._send_json({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, 500)
    
    def do_GET(self):
        """GET no soportado para este endpoint."""
        self._send_json({'error': 'Use POST method'}, 405)
    
    def _extract_drive_file_id(self, url):
        """Extrae el ID de archivo de una URL de Google Drive."""
        if not url:
            return None
        
        # Patrones comunes de URLs de Drive
        patterns = [
            r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
            r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
            r'docs\.google\.com/document/d/([a-zA-Z0-9_-]+)',
            r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)',
            r'docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)',
            r'/d/([a-zA-Z0-9_-]+)(?:/|\?|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                file_id = match.group(1)
                if len(file_id) >= 25:
                    return file_id
        
        return None
    
    def _download_drive_file(self, file_id, access_token, name):
        """Descarga un archivo de Drive usando el token del usuario."""
        # Primero obtener metadata
        metadata_url = f'https://www.googleapis.com/drive/v3/files/{file_id}?fields=name,mimeType'
        
        try:
            meta_req = urllib.request.Request(
                metadata_url,
                headers={'Authorization': f'Bearer {access_token}'}
            )
            with urllib.request.urlopen(meta_req, timeout=10) as response:
                metadata = json.loads(response.read().decode('utf-8'))
                real_name = metadata.get('name', name)
                mime_type = metadata.get('mimeType', '')
        except:
            real_name = name
            mime_type = ''
        
        # Determinar URL de descarga según el tipo
        if 'google-apps.document' in mime_type:
            download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/pdf'
            if not real_name.endswith('.pdf'):
                real_name = real_name + '.pdf'
        elif 'google-apps.spreadsheet' in mime_type:
            download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            if not real_name.endswith('.xlsx'):
                real_name = real_name + '.xlsx'
        elif 'google-apps.presentation' in mime_type:
            download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/pdf'
            if not real_name.endswith('.pdf'):
                real_name = real_name + '.pdf'
        else:
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
        except Exception as e:
            return (None, real_name)
    
    def _get_cookie(self, name):
        """Extrae una cookie por nombre."""
        cookie_header = self.headers.get('Cookie', '') if self.headers else ''
        for cookie in cookie_header.split(';'):
            cookie = cookie.strip()
            if cookie.startswith(f'{name}='):
                return cookie.split('=', 1)[1]
        return None
    
    def _send_json(self, data, status=200):
        """Envía respuesta JSON."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        """Silenciar logs."""
        pass
