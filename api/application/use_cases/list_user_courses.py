"""
List User Courses Use Case - Classroom Explorer

Caso de uso para listar los cursos de un usuario.

POR QUÉ SÍ separar en Use Case:
✅ Encapsula la lógica de la operación
✅ Fácil de testear (mock del repositorio)
✅ Reutilizable desde diferentes puntos (API, CLI, etc.)
✅ Single Responsibility Principle

POR QUÉ NO poner lógica directamente en el route:
❌ Routes se vuelven gordos
❌ Difícil de testear
❌ No es reutilizable
"""

from typing import List, Optional
from dataclasses import dataclass
from api.domain.entities import Course, CourseState
from api.domain.interfaces import ClassroomRepository


@dataclass
class ListUserCoursesRequest:
    """
    Request DTO para el caso de uso.
    
    Un DTO (Data Transfer Object) es un objeto simple
    que transporta datos entre capas.
    """
    user_id: str
    access_token: str
    include_archived: bool = True
    filter_state: Optional[CourseState] = None


@dataclass
class ListUserCoursesResponse:
    """
    Response DTO para el caso de uso.
    
    Incluye los cursos y metadatos adicionales.
    """
    courses: List[Course]
    total_count: int
    active_count: int
    archived_count: int


class ListUserCourses:
    """
    Use Case: Listar cursos del usuario.
    
    Orquesta:
    1. Obtener cursos del repositorio
    2. Filtrar según parámetros
    3. Retornar con metadatos
    """
    
    def __init__(self, repository: ClassroomRepository):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            repository: Repositorio para obtener cursos
        
        POR QUÉ SÍ Dependency Injection:
        • El use case no crea el repositorio
        • Permite inyectar un mock para testing
        • Desacoplamiento total
        """
        self.repository = repository
    
    def execute(self, request: ListUserCoursesRequest) -> ListUserCoursesResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            request: Parámetros de la solicitud
        
        Returns:
            ListUserCoursesResponse con cursos y metadatos
        
        Example:
            >>> use_case = ListUserCourses(repository)
            >>> request = ListUserCoursesRequest(
            ...     user_id="123",
            ...     access_token="token...",
            ...     include_archived=True
            ... )
            >>> response = use_case.execute(request)
            >>> print(f"Total: {response.total_count}")
        """
        # 1. Obtener todos los cursos del usuario
        all_courses = self.repository.get_user_courses(
            user_id=request.user_id,
            access_token=request.access_token
        )
        
        # 2. Filtrar cursos según parámetros
        filtered_courses = self._apply_filters(
            courses=all_courses,
            include_archived=request.include_archived,
            filter_state=request.filter_state
        )
        
        # 3. Calcular estadísticas
        active_count = sum(1 for c in all_courses if c.state == CourseState.ACTIVE)
        archived_count = sum(1 for c in all_courses if c.state == CourseState.ARCHIVED)
        
        return ListUserCoursesResponse(
            courses=filtered_courses,
            total_count=len(all_courses),
            active_count=active_count,
            archived_count=archived_count
        )
    
    def _apply_filters(
        self,
        courses: List[Course],
        include_archived: bool,
        filter_state: Optional[CourseState]
    ) -> List[Course]:
        """
        Aplica filtros a la lista de cursos.
        
        Args:
            courses: Lista original
            include_archived: Si incluir archivados
            filter_state: Filtrar por estado específico
        
        Returns:
            Lista filtrada
        """
        result = courses
        
        # Filtrar por estado específico
        if filter_state:
            result = [c for c in result if c.state == filter_state]
        
        # Excluir archivados si no se quieren
        if not include_archived:
            result = [c for c in result if c.state != CourseState.ARCHIVED]
        
        # Solo mostrar cursos visibles (ACTIVE o ARCHIVED)
        result = [c for c in result if c.is_visible()]
        
        return result
