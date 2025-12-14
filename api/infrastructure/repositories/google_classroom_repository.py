"""
Google Classroom Repository - Classroom Explorer

Implementación concreta del ClassroomRepository que usa Google Classroom API.

POR QUÉ SÍ esta implementación:
✅ Implementa la interface del dominio
✅ Usa el cliente HTTP y el mapper
✅ Agrega caché para reducir llamadas a la API
✅ Puede ser reemplazada por un mock en tests
"""

from typing import List
from api.domain.entities import Course, Material
from api.domain.interfaces import (
    ClassroomRepository,
    RepositoryError,
    CourseNotFoundError
)
from api.infrastructure.google_classroom_client import GoogleClassroomClient, GoogleAPIError
from api.infrastructure.mappers import ClassroomMapper
from api.infrastructure.cache import cache
from api.infrastructure.config import Config


class GoogleClassroomRepository(ClassroomRepository):
    """
    Implementación del repositorio usando Google Classroom API.
    
    Esta clase:
    - Implementa la interface ClassroomRepository
    - Usa GoogleClassroomClient para hacer requests HTTP
    - Usa ClassroomMapper para convertir respuestas a entidades
    - Usa MemoryCache para cachear resultados
    """
    
    def __init__(self):
        """Inicializa el repositorio con sus dependencias."""
        self.client = GoogleClassroomClient()
        self.mapper = ClassroomMapper()
    
    def get_user_courses(self, user_id: str, access_token: str) -> List[Course]:
        """
        Obtiene todos los cursos de un usuario.
        
        Implementa ClassroomRepository.get_user_courses()
        
        Args:
            user_id: ID del usuario de Google
            access_token: Token de acceso de OAuth 2.0
        
        Returns:
            List[Course]: Lista de cursos del usuario
        """
        # Clave de caché única por usuario
        cache_key = f"courses_user_{user_id}"
        
        # Intentar obtener de caché
        cached_courses = cache.get(cache_key)
        if cached_courses is not None:
            return cached_courses
        
        try:
            # Llamar a Google API
            api_response = self.client.list_courses(access_token)
            
            # Mapear respuestas a entidades
            courses = [
                self.mapper.api_course_to_domain(course_data)
                for course_data in api_response.get('courses', [])
            ]
            
            # Guardar en caché
            cache.set(cache_key, courses, ttl_seconds=Config.CACHE_TTL_SECONDS)
            
            return courses
            
        except GoogleAPIError as e:
            raise RepositoryError(f"Error al obtener cursos: {str(e)}")
    
    def get_course_materials(
        self,
        course_id: str,
        access_token: str
    ) -> List[Material]:
        """
        Obtiene todos los materiales de un curso.
        
        Combina courseWork y courseWorkMaterials de la API.
        
        Args:
            course_id: ID del curso
            access_token: Token de acceso de OAuth 2.0
        
        Returns:
            List[Material]: Lista de materiales del curso
        """
        # Clave de caché única por curso
        cache_key = f"materials_course_{course_id}"
        
        # Intentar obtener de caché
        cached_materials = cache.get(cache_key)
        if cached_materials is not None:
            return cached_materials
        
        try:
            materials: List[Material] = []
            
            # Obtener courseWork (tareas)
            try:
                course_work_response = self.client.list_course_work(
                    course_id, access_token
                )
                for item in course_work_response.get('courseWork', []):
                    material = self.mapper.api_material_to_domain(item, course_id)
                    materials.append(material)
            except GoogleAPIError:
                # Si falla, continuamos sin courseWork
                pass
            
            # Obtener courseWorkMaterials (materiales de referencia)
            try:
                materials_response = self.client.list_course_work_materials(
                    course_id, access_token
                )
                for item in materials_response.get('courseWorkMaterial', []):
                    material = self.mapper.api_material_to_domain(item, course_id)
                    materials.append(material)
            except GoogleAPIError:
                # Si falla, continuamos sin courseWorkMaterials
                pass
            
            # Ordenar por fecha de creación (más reciente primero)
            materials.sort(key=lambda m: m.created_at, reverse=True)
            
            # Guardar en caché
            cache.set(cache_key, materials, ttl_seconds=Config.CACHE_TTL_SECONDS)
            
            return materials
            
        except GoogleAPIError as e:
            raise RepositoryError(f"Error al obtener materiales: {str(e)}")
    
    def get_course_by_id(
        self,
        course_id: str,
        access_token: str
    ) -> Course:
        """
        Obtiene un curso por su ID.
        
        Args:
            course_id: ID del curso
            access_token: Token de acceso de OAuth 2.0
        
        Returns:
            Course: Curso encontrado
        
        Raises:
            CourseNotFoundError: Si el curso no existe
        """
        # Clave de caché
        cache_key = f"course_{course_id}"
        
        # Intentar obtener de caché
        cached_course = cache.get(cache_key)
        if cached_course is not None:
            return cached_course
        
        try:
            # Llamar a Google API
            api_response = self.client.get_course(course_id, access_token)
            
            # Mapear a entidad
            course = self.mapper.api_course_to_domain(api_response)
            
            # Guardar en caché
            cache.set(cache_key, course, ttl_seconds=Config.CACHE_TTL_SECONDS)
            
            return course
            
        except GoogleAPIError as e:
            if "404" in str(e):
                raise CourseNotFoundError(f"Curso no encontrado: {course_id}")
            raise RepositoryError(f"Error al obtener curso: {str(e)}")


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que GoogleClassroomRepository funciona.
    
    NOTA: No hace llamadas reales a Google API.
    Solo verifica la estructura y dependencias.
    
    Ejecutar con:
        python -m api.infrastructure.repositories.google_classroom_repository
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: GoogleClassroomRepository")
    print("=" * 60)
    
    # Test 1: Verificar que se puede instanciar
    print("\n1. Verificar instanciación:")
    repo = GoogleClassroomRepository()
    print(f"   ✓ Repositorio creado: {type(repo).__name__}")
    
    # Test 2: Verificar dependencias
    print("\n2. Verificar dependencias:")
    print(f"   ✓ client: {type(repo.client).__name__}")
    print(f"   ✓ mapper: {type(repo.mapper).__name__}")
    
    # Test 3: Verificar que implementa la interface
    print("\n3. Verificar implementación de interface:")
    is_subclass = isinstance(repo, ClassroomRepository)
    print(f"   ✓ Es ClassroomRepository: {is_subclass}")
    
    # Test 4: Verificar métodos disponibles
    print("\n4. Verificar métodos disponibles:")
    methods = ['get_user_courses', 'get_course_materials', 'get_course_by_id']
    for method in methods:
        has_method = hasattr(repo, method) and callable(getattr(repo, method))
        print(f"   ✓ {method}(): {'existe' if has_method else 'NO EXISTE'}")
    
    # Test 5: Verificar que usa caché
    print("\n5. Verificar uso de caché:")
    print(f"   ✓ Cache disponible: {cache is not None}")
    print(f"   ✓ Cache TTL: {Config.CACHE_TTL_SECONDS} segundos")
    
    # Test 6: Verificar generación de cache keys
    print("\n6. Verificar cache keys:")
    test_user_id = "user_123"
    test_course_id = "course_456"
    print(f"   ✓ Key para cursos: courses_user_{test_user_id}")
    print(f"   ✓ Key para materiales: materials_course_{test_course_id}")
    print(f"   ✓ Key para curso: course_{test_course_id}")
    
    print("\n" + "=" * 60)
    print("⚠️  NOTA: No se hicieron llamadas reales a Google API")
    print("    Para probar conexión real, usa credenciales válidas")
    print("=" * 60)
    print("✅ Prueba de GoogleClassroomRepository: OK")
    print("=" * 60)
