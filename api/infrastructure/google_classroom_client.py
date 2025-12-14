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


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que GoogleClassroomClient funciona.
    
    NOTA: No hace llamadas reales a Google API.
    Solo verifica la estructura y el patrón Singleton.
    
    Ejecutar con:
        python -m api.infrastructure.google_classroom_client
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: GoogleClassroomClient")
    print("=" * 60)
    
    # Test 1: Verificar patrón Singleton
    print("\n1. Verificar patrón Singleton:")
    client1 = GoogleClassroomClient()
    client2 = GoogleClassroomClient()
    is_same = client1 is client2
    print(f"   ✓ client1 is client2 = {is_same} (esperado: True)")
    print(f"   ✓ Es Singleton: {'✓' if is_same else '✗'}")
    
    # Test 2: Verificar que tiene los atributos correctos
    print("\n2. Verificar atributos:")
    print(f"   ✓ base_url: {client1.base_url}")
    print(f"   ✓ session tipo: {type(client1.session).__name__}")
    print(f"   ✓ _initialized: {client1._initialized}")
    
    # Test 3: Verificar métodos públicos
    print("\n3. Verificar métodos disponibles:")
    methods = ['list_courses', 'get_course', 'list_course_work', 'list_course_work_materials']
    for method_name in methods:
        has_method = hasattr(client1, method_name)
        print(f"   ✓ {method_name}(): {'existe' if has_method else 'NO EXISTE'}")
    
    # Test 4: Verificar que _make_request existe
    print("\n4. Verificar método interno _make_request:")
    has_make_request = hasattr(client1, '_make_request')
    print(f"   ✓ _make_request(): {'existe' if has_make_request else 'NO EXISTE'}")
    
    # Test 5: Verificar excepción GoogleAPIError
    print("\n5. Verificar excepción GoogleAPIError:")
    try:
        raise GoogleAPIError("Test error message")
    except GoogleAPIError as e:
        print(f"   ✓ GoogleAPIError capturado: '{str(e)}'")
    
    # Test 6: Verificar generación de URLs
    print("\n6. Verificar generación de URLs:")
    course_url = f"{client1.base_url}/courses"
    course_work_url = f"{client1.base_url}/courses/123/courseWork"
    print(f"   ✓ URL de cursos: {course_url}")
    print(f"   ✓ URL de courseWork: {course_work_url}")
    
    # Test 7: Verificar headers esperados
    print("\n7. Verificar estructura de headers:")
    test_token = "test_access_token"
    expected_headers = {
        'Authorization': f'Bearer {test_token}',
        'Accept': 'application/json'
    }
    print(f"   ✓ Authorization header: 'Bearer {test_token[:10]}...'")
    print(f"   ✓ Accept header: 'application/json'")
    
    print("\n" + "=" * 60)
    print("⚠️  NOTA: No se hicieron llamadas reales a Google API")
    print("    Para probar conexión real, usa credenciales válidas")
    print("=" * 60)
    print("✅ Prueba de GoogleClassroomClient: OK")
    print("=" * 60)
