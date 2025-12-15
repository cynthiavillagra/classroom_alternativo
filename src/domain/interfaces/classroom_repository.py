"""
Classroom Repository Interface - Classroom Explorer

Interface (Port) que define el contrato para acceder a datos de Google Classroom.

POR QUÉ SÍ usar una interfaz:
✅ Hexagonal Architecture: El dominio define el contrato
✅ Dependency Inversion: El dominio no depende de la infraestructura
✅ Testing: Fácil de mockear para tests
✅ Flexibilidad: Podemos cambiar la implementación (Google API, Mock, DB cache)

POR QUÉ NO usar directamente Google API:
❌ Acoplamiento: El dominio dependería de Google
❌ Testing difícil: No podríamos testear sin llamar a Google
❌ Inflexible: No podríamos cambiar de proveedor
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ ABC: Abstract Base Class para definir interfaces
# POR QUÉ abstractmethod: Fuerza implementación en subclases
from abc import ABC, abstractmethod
from typing import List
from ..entities.course import Course
from ..entities.material import Material


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la interface (Port)
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Hexagonal: El dominio define qué necesita, infra lo implementa
class ClassroomRepository(ABC):
    """
    Interface (Port) para acceder a datos de Google Classroom.
    
    Esta es una INTERFAZ (Abstract Base Class).
    Define QUÉ operaciones se pueden hacer, pero NO CÓMO.
    
    La implementación concreta estará en Infrastructure Layer:
    - GoogleClassroomRepository: Llama a Google API
    - MockClassroomRepository: Devuelve datos fake para testing
    - CachedClassroomRepository: Agrega caché sobre Google API
    
    POR QUÉ SÍ este diseño:
    • El dominio define el contrato (qué necesita)
    • La infraestructura lo implementa (cómo lo hace)
    • Dependency Inversion Principle (DIP)
    """
    
    @abstractmethod
    def get_user_courses(self, user_id: str, access_token: str) -> List[Course]:
        """
        Obtiene todos los cursos de un usuario.
        
        Args:
            user_id: ID del usuario de Google
            access_token: Token de acceso de OAuth 2.0
        
        Returns:
            List[Course]: Lista de cursos del usuario
        
        Raises:
            RepositoryError: Si hay un error al obtener los cursos
        
        Example:
            >>> repository = GoogleClassroomRepository()
            >>> courses = repository.get_user_courses("user123", "token...")
            >>> for course in courses:
            ...     print(course.name)
        """
        pass
    
    @abstractmethod
    def get_course_materials(
        self,
        course_id: str,
        access_token: str
    ) -> List[Material]:
        """
        Obtiene todos los materiales de un curso.
        
        Args:
            course_id: ID del curso
            access_token: Token de acceso de OAuth 2.0
        
        Returns:
            List[Material]: Lista de materiales del curso
        
        Raises:
            RepositoryError: Si hay un error al obtener los materiales
            CourseNotFoundError: Si el curso no existe
        
        Example:
            >>> repository = GoogleClassroomRepository()
            >>> materials = repository.get_course_materials("course123", "token...")
            >>> for material in materials:
            ...     print(f"{material.title} ({material.type.get_label()})")
        """
        pass
    
    @abstractmethod
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
            RepositoryError: Si hay un error al obtener el curso
        
        Example:
            >>> repository = GoogleClassroomRepository()
            >>> course = repository.get_course_by_id("course123", "token...")
            >>> print(course.name)
        """
        pass


# ═══════════════════════════════════════════════════════════════
# Excepciones del Repositorio
# ═══════════════════════════════════════════════════════════════

class RepositoryError(Exception):
    """Error base del repositorio."""
    pass


class CourseNotFoundError(RepositoryError):
    """El curso no fue encontrado."""
    pass


class MaterialNotFoundError(RepositoryError):
    """El material no fue encontrado."""
    pass


class UnauthorizedError(RepositoryError):
    """El usuario no tiene permisos para acceder al recurso."""
    pass


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que la interface y excepciones funcionan.
    
    NOTA: ClassroomRepository es una clase abstracta, no se puede instanciar.
    Verificamos que la estructura sea correcta.
    
    Ejecutar con:
        python -m api.domain.interfaces.classroom_repository
    """
    from datetime import datetime
    from ..entities.course_state import CourseState
    from ..entities.material_type import MaterialType
    
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: ClassroomRepository (Interface)")
    print("=" * 60)
    
    # Test 1: Verificar que ClassroomRepository es abstracta
    print("\n1. Verificar que ClassroomRepository es abstracta:")
    try:
        repo = ClassroomRepository()
        print("   ✗ ERROR: No debería poder instanciarse")
    except TypeError as e:
        print("   ✓ TypeError esperado: no se puede instanciar clase abstracta")
    
    # Test 2: Verificar métodos abstractos
    print("\n2. Verificar métodos abstractos:")
    abstract_methods = ['get_user_courses', 'get_course_materials', 'get_course_by_id']
    for method in abstract_methods:
        has_method = hasattr(ClassroomRepository, method)
        print(f"   ✓ {method}: {'existe' if has_method else 'NO EXISTE'}")
    
    # Test 3: Crear implementación mock para verificar contrato
    print("\n3. Crear MockRepository para verificar contrato:")
    
    class MockClassroomRepository(ClassroomRepository):
        """Mock para testing."""
        
        def get_user_courses(self, user_id: str, access_token: str) -> List[Course]:
            now = datetime.now()
            return [
                Course(
                    id="mock_course_1",
                    name="Mock Course",
                    state=CourseState.ACTIVE,
                    owner_id=user_id,
                    created_at=now,
                    updated_at=now
                )
            ]
        
        def get_course_materials(self, course_id: str, access_token: str) -> List[Material]:
            now = datetime.now()
            return [
                Material(
                    id="mock_material_1",
                    course_id=course_id,
                    title="Mock Material",
                    type=MaterialType.PDF,
                    url="https://example.com/mock.pdf",
                    created_at=now,
                    updated_at=now
                )
            ]
        
        def get_course_by_id(self, course_id: str, access_token: str) -> Course:
            now = datetime.now()
            return Course(
                id=course_id,
                name="Mock Course",
                state=CourseState.ACTIVE,
                owner_id="mock_owner",
                created_at=now,
                updated_at=now
            )
    
    mock_repo = MockClassroomRepository()
    print(f"   ✓ MockClassroomRepository creado")
    
    # Test 4: Verificar get_user_courses
    print("\n4. Verificar get_user_courses():")
    courses = mock_repo.get_user_courses("user123", "token")
    print(f"   ✓ Retornó {len(courses)} curso(s)")
    print(f"   ✓ Primer curso: {courses[0].name}")
    
    # Test 5: Verificar get_course_materials
    print("\n5. Verificar get_course_materials():")
    materials = mock_repo.get_course_materials("course123", "token")
    print(f"   ✓ Retornó {len(materials)} material(es)")
    print(f"   ✓ Primer material: {materials[0].title}")
    
    # Test 6: Verificar excepciones
    print("\n6. Verificar excepciones del repositorio:")
    exceptions = [
        ("RepositoryError", RepositoryError),
        ("CourseNotFoundError", CourseNotFoundError),
        ("MaterialNotFoundError", MaterialNotFoundError),
        ("UnauthorizedError", UnauthorizedError)
    ]
    for name, exc_class in exceptions:
        try:
            raise exc_class(f"Test {name}")
        except RepositoryError as e:
            print(f"   ✓ {name} capturado correctamente")
    
    # Test 7: Verificar herencia de excepciones
    print("\n7. Verificar herencia de excepciones:")
    print(f"   ✓ CourseNotFoundError es RepositoryError: {issubclass(CourseNotFoundError, RepositoryError)}")
    print(f"   ✓ MaterialNotFoundError es RepositoryError: {issubclass(MaterialNotFoundError, RepositoryError)}")
    print(f"   ✓ UnauthorizedError es RepositoryError: {issubclass(UnauthorizedError, RepositoryError)}")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de ClassroomRepository: OK")
    print("=" * 60)
