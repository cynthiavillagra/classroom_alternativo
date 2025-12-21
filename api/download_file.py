"""
Vercel Serverless Function: Download Single File
Endpoint GET /api/download_file?url=...&name=...&date=...

[FIX v1.3.3] Descarga un archivo individual con prefijo de fecha.
"""

from http.server import BaseHTTPRequestHandler
import json
import re
from urllib.parse import parse_qs, urlparse


class handler(BaseHTTPRequestHandler):
    """Handler para descargar un archivo individual con prefijo de fecha."""
    
    def do_GET(self):
        """Maneja GET /api/download_file."""
        try:
            # Parsear query params
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            url = params.get('url', [''])[0]
            name = params.get('name', ['archivo'])[0]
            file_date = params.get('date', [''])[0]
            
            if not url:
                self._send_json({'error': 'URL required'}, 400)
                return
            
            # Obtener token de cookie
            access_token = self._get_cookie('access_token')
            
            if not access_token:
                self._send_json({'error': 'Not authenticated'}, 401)
                return
            
            # Extraer file ID
            file_id = self._extract_drive_file_id(url)
            
            if not file_id:
                self._send_json({'error': 'Could not extract file ID from URL'}, 400)
                return
            
            # [FIX v1.3.6] Formatear prefijo usando hora Argentina (UTC-3)
            # Para evitar que archivos subidos a la noche aparezcan con fecha del día siguiente
            date_prefix = ''
            if file_date:
                try:
                    from datetime import datetime, timedelta, timezone
                    # Parsear fecha ISO (asumiendo UTC si termina en Z)
                    if file_date.endswith('Z'):
                        # Python < 3.11 no soporta Z con fromisoformat bien a veces, reemplazamos
                        dt_utc = datetime.fromisoformat(file_date.replace('Z', '+00:00'))
                    else:
                        dt_utc = datetime.fromisoformat(file_date)
                    
                    # Convertir a UTC-3
                    tz_arg = timezone(timedelta(hours=-3))
                    dt_arg = dt_utc.astimezone(tz_arg)
                    
                    date_prefix = dt_arg.strftime('%Y-%m-%d_')
                except Exception as e:
                    # Fallback a regex si falla el parseo
                    import re
                    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', file_date)
                    if date_match:
                        date_prefix = date_match.group(1) + '_'
            
            # Descargar archivo
            file_content, filename = self._download_file(file_id, access_token, name)
            
            if not file_content:
                self._send_json({'error': 'Could not download file'}, 500)
                return
            
            # Agregar prefijo de fecha
            prefixed_filename = f"{date_prefix}{filename}"
            
            # Enviar archivo
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{prefixed_filename}"')
            self.send_header('Content-Length', str(len(file_content)))
            self.end_headers()
            self.wfile.write(file_content)
            
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
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
            with urllib.request.urlopen(req, timeout=60) as resp:
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
