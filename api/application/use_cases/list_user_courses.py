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


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que ListUserCourses funciona.
    
    Ejecutar con:
        python -m api.application.use_cases.list_user_courses
    """
    from datetime import datetime
    from api.domain.entities import Course
    from api.domain.factories import CourseFactory
    
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: ListUserCourses")
    print("=" * 60)
    
    # Crear Mock Repository
    class MockRepository(ClassroomRepository):
        """Mock para testing."""
        
        def get_user_courses(self, user_id: str, access_token: str) -> List[Course]:
            now = datetime.now()
            return [
                CourseFactory.create_for_testing(
                    id="course_1",
                    name="Matemáticas",
                    state=CourseState.ACTIVE
                ),
                CourseFactory.create_for_testing(
                    id="course_2",
                    name="Historia",
                    state=CourseState.ACTIVE
                ),
                CourseFactory.create_for_testing(
                    id="course_3",
                    name="Física (Archivado)",
                    state=CourseState.ARCHIVED
                ),
            ]
        
        def get_course_materials(self, course_id: str, access_token: str):
            return []
        
        def get_course_by_id(self, course_id: str, access_token: str):
            return None
    
    mock_repo = MockRepository()
    use_case = ListUserCourses(mock_repo)
    
    # Test 1: Ejecutar con todos los cursos
    print("\n1. Ejecutar con include_archived=True:")
    request = ListUserCoursesRequest(
        user_id="user_123",
        access_token="token",
        include_archived=True
    )
    response = use_case.execute(request)
    print(f"   ✓ Total: {response.total_count}")
    print(f"   ✓ Activos: {response.active_count}")
    print(f"   ✓ Archivados: {response.archived_count}")
    print(f"   ✓ Cursos retornados: {len(response.courses)}")
    
    # Test 2: Ejecutar sin archivados
    print("\n2. Ejecutar con include_archived=False:")
    request2 = ListUserCoursesRequest(
        user_id="user_123",
        access_token="token",
        include_archived=False
    )
    response2 = use_case.execute(request2)
    print(f"   ✓ Cursos retornados: {len(response2.courses)} (esperado: 2)")
    
    # Test 3: Filtrar solo por ACTIVE
    print("\n3. Filtrar solo ACTIVE:")
    request3 = ListUserCoursesRequest(
        user_id="user_123",
        access_token="token",
        filter_state=CourseState.ACTIVE
    )
    response3 = use_case.execute(request3)
    print(f"   ✓ Cursos ACTIVE: {len(response3.courses)} (esperado: 2)")
    
    # Test 4: Verificar DTOs
    print("\n4. Verificar DTOs:")
    print(f"   ✓ ListUserCoursesRequest tiene: user_id, access_token, include_archived, filter_state")
    print(f"   ✓ ListUserCoursesResponse tiene: courses, total_count, active_count, archived_count")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de ListUserCourses: OK")
    print("=" * 60)
