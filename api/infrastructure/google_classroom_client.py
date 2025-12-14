"""
Google Classroom HTTP Client - Classroom Explorer

Cliente HTTP para interactuar con Google Classroom API.

POR QUÉ SÍ Singleton:
✅ Reutiliza la sesión HTTP (conexiones persistentes)
✅ Evita crear múltiples instancias
✅ Gestiona rate limiting centralizadamente

POR QUÉ NO crear una instancia por request:
❌ Overhead de crear sesiones HTTP
❌ No se reutilizan conexiones
❌ Más lento
"""

import requests
import time
from typing import Dict, Any, Optional
from .config import Config


class GoogleClassroomClient:
    """
    Cliente HTTP Singleton para Google Classroom API.
    
    Maneja:
    - Requests HTTP a Google API
    - Retry con backoff exponencial
    - Rate limiting
    - Errores de API
    """
    
    _instance: Optional['GoogleClassroomClient'] = None
    
    def __new__(cls):
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa el cliente (solo una vez)."""
        if self._initialized:
            return
        
        self.base_url = Config.CLASSROOM_API_BASE_URL
        self.session = requests.Session()
        self._initialized = True
    
    def list_courses(self, access_token: str) -> Dict[str, Any]:
        """
        Lista todos los cursos del usuario.
        
        Args:
            access_token: Token de acceso de OAuth 2.0
        
        Returns:
            dict: Respuesta de la API con lista de cursos
        
        Raises:
            GoogleAPIError: Si hay un error en la API
        """
        url = f"{self.base_url}/courses"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        return self._make_request('GET', url, headers)
    
    def get_course(self, course_id: str, access_token: str) -> Dict[str, Any]:
        """
        Obtiene un curso por ID.
        
        Args:
            course_id: ID del curso
            access_token: Token de acceso
        
        Returns:
            dict: Datos del curso
        """
        url = f"{self.base_url}/courses/{course_id}"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        return self._make_request('GET', url, headers)
    
    def list_course_work(
        self,
        course_id: str,
        access_token: str
    ) -> Dict[str, Any]:
        """
        Lista las tareas (courseWork) de un curso.
        
        Args:
            course_id: ID del curso
            access_token: Token de acceso
        
        Returns:
            dict: Respuesta con lista de courseWork
        """
        url = f"{self.base_url}/courses/{course_id}/courseWork"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        return self._make_request('GET', url, headers)
    
    def list_course_work_materials(
        self,
        course_id: str,
        access_token: str
    ) -> Dict[str, Any]:
        """
        Lista los materiales (courseWorkMaterials) de un curso.
        
        Args:
            course_id: ID del curso
            access_token: Token de acceso
        
        Returns:
            dict: Respuesta con lista de courseWorkMaterials
        """
        url = f"{self.base_url}/courses/{course_id}/courseWorkMaterials"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        return self._make_request('GET', url, headers)
    
    def _make_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Hace un request HTTP con retry y backoff exponencial.
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            url: URL completa
            headers: Headers HTTP
            max_retries: Número máximo de reintentos
        
        Returns:
            dict: Respuesta JSON de la API
        
        Raises:
            GoogleAPIError: Si falla después de todos los reintentos
        """
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    timeout=10
                )
                
                # Manejar rate limiting (429)
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 5))
                    time.sleep(retry_after)
                    continue
                
                # Manejar errores 5xx (servidor)
                if 500 <= response.status_code < 600:
                    if attempt < max_retries - 1:
                        # Backoff exponencial: 1s, 2s, 4s
                        time.sleep(2 ** attempt)
                        continue
                
                # Lanzar excepción si no es 2xx
                response.raise_for_status()
                
                # Retornar JSON
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise GoogleAPIError(f"Error al llamar a Google API: {str(e)}")
                time.sleep(2 ** attempt)
        
        raise GoogleAPIError("Máximo de reintentos alcanzado")


# ═══════════════════════════════════════════════════════════════
# Excepciones
# ═══════════════════════════════════════════════════════════════

class GoogleAPIError(Exception):
    """Error al llamar a Google Classroom API."""
    pass
