"""
Vercel Serverless Function: Download ZIP
Endpoint POST /api/download_zip

[FIX v1.2.4] Simplificado para debugging.
"""

from http.server import BaseHTTPRequestHandler
import json
import zipfile
import io
import re

# Imports condicionales para robustez
try:
    import urllib.request
    import urllib.error
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
                    file_date = file_info.get('date', '')  # [FIX v1.3.1] Obtener fecha
                    
                    # [FIX v1.3.6] Formatear prefijo usando hora Argentina (UTC-3)
                    date_prefix = ''
                    if file_date:
                        try:
                            from datetime import datetime, timedelta, timezone
                            if file_date.endswith('Z'):
                                dt_utc = datetime.fromisoformat(file_date.replace('Z', '+00:00'))
                            else:
                                dt_utc = datetime.fromisoformat(file_date)
                            
                            tz_arg = timezone(timedelta(hours=-3))
                            dt_arg = dt_utc.astimezone(tz_arg)
                            date_prefix = dt_arg.strftime('%Y-%m-%d_')
                        except:
                            # Fallback regex
                            import re
                            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', file_date)
                            if date_match:
                                date_prefix = date_match.group(1) + '_'
                    
                    # Extraer ID del archivo de Drive
                    file_id = self._extract_drive_file_id(url)
                    
                    if file_id:
                        try:
                            # Descargar archivo
                            file_content, filename = self._download_file(file_id, access_token, name)
                            
                            if file_content:
                                # [FIX v1.3.1] Agregar prefijo de fecha
                                prefixed_filename = f"{date_prefix}{filename}"
                                zip_file.writestr(prefixed_filename, file_content)
                            else:
                                error_content = f"No se pudo descargar: {name}\nURL: {url}\n"
                                zip_file.writestr(f"{name}_ERROR.txt", error_content)
                        except Exception as e:
                            error_content = f"Error: {name}\nURL: {url}\nError: {str(e)}\n"
                            zip_file.writestr(f"{name}_ERROR.txt", error_content)
                    else:
                        # No se pudo extraer el ID, guardar link
                        link_content = f"[InternetShortcut]\nURL={url}\n"
                        prefixed_name = f"{date_prefix}{name}" if date_prefix else name
                        zip_file.writestr(f"{prefixed_name}.url", link_content)
            
            # Enviar ZIP
            zip_buffer.seek(0)
            zip_content = zip_buffer.read()
            
            # Sanitizar nombre del archivo
            safe_name = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in course_name)
            filename = f"{safe_name}.zip"
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-Length', str(len(zip_content)))
            self.end_headers()
            self.wfile.write(zip_content)
            
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
    def do_GET(self):
        """GET retorna info del endpoint."""
        self._send_json({
            'endpoint': '/api/download_zip',
            'method': 'POST',
            'status': 'ready'
        })
    
    def _extract_drive_file_id(self, url):
        """Extrae el ID de archivo de una URL de Google Drive."""
        if not url:
            return None
        
        patterns = [
            r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
            r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
            r'docs\.google\.com/document/d/([a-zA-Z0-9_-]+)',
            r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)',
            r'docs\.google\.com/presentation/d/([a-zA-Z0-9_-]+)',
            r'/d/([a-zA-Z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                file_id = match.group(1)
                if len(file_id) >= 20:
                    return file_id
        
        return None
    
    def _download_file(self, file_id, access_token, name):
        """Descarga un archivo de Drive."""
        import urllib.request
        import urllib.error
        
        # Obtener metadata
        try:
            meta_url = f'https://www.googleapis.com/drive/v3/files/{file_id}?fields=name,mimeType'
            meta_req = urllib.request.Request(meta_url, headers={'Authorization': f'Bearer {access_token}'})
            with urllib.request.urlopen(meta_req, timeout=10) as resp:
                meta = json.loads(resp.read().decode())
                real_name = meta.get('name', name)
                mime = meta.get('mimeType', '')
        except:
            real_name = name
            mime = ''
        
        # Determinar URL de descarga
        if 'google-apps.document' in mime:
            dl_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/pdf'
            real_name = real_name + '.pdf' if not real_name.endswith('.pdf') else real_name
        elif 'google-apps.spreadsheet' in mime:
            dl_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            real_name = real_name + '.xlsx' if not real_name.endswith('.xlsx') else real_name
        elif 'google-apps.presentation' in mime:
            dl_url = f'https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType=application/pdf'
            real_name = real_name + '.pdf' if not real_name.endswith('.pdf') else real_name
        else:
            dl_url = f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media'
        
        # Descargar
        try:
            req = urllib.request.Request(dl_url, headers={'Authorization': f'Bearer {access_token}'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return (resp.read(), real_name)
        except:
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
        pass
