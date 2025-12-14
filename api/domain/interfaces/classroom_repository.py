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

from abc import ABC, abstractmethod
from typing import List
from ..entities.course import Course
from ..entities.material import Material


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
