"""
List Course Materials Use Case - Classroom Explorer

Caso de uso para listar los materiales de un curso.
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Material + MaterialType: Entidades del dominio
# POR QUÉ ClassroomRepository: Dependency Injection
from typing import List, Optional
from dataclasses import dataclass
from src.domain.entities import Material, MaterialType
from src.domain.interfaces import ClassroomRepository


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir DTOs (Data Transfer Objects)
# ═══════════════════════════════════════════════════════════════
# POR QUÉ DTOs separados: Encapsulan entrada/salida del Use Case
@dataclass
class ListCourseMaterialsRequest:
    """Request DTO para el caso de uso."""
    course_id: str
    access_token: str
    filter_type: Optional[MaterialType] = None
    search_query: Optional[str] = None
    limit: Optional[int] = None


@dataclass
class ListCourseMaterialsResponse:
    """Response DTO para el caso de uso."""
    materials: List[Material]
    total_count: int
    filtered_count: int
    type_counts: dict  # Conteo por tipo


class ListCourseMaterials:
    """
    Use Case: Listar materiales de un curso.
    
    Orquesta:
    1. Obtener materiales del repositorio
    2. Aplicar filtros (tipo, búsqueda)
    3. Retornar con metadatos
    """
    
    def __init__(self, repository: ClassroomRepository):
        """
        Inicializa con Dependency Injection.
        
        Args:
            repository: Repositorio para obtener materiales
        """
        self.repository = repository
    
    def execute(self, request: ListCourseMaterialsRequest) -> ListCourseMaterialsResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            request: Parámetros de la solicitud
        
        Returns:
            ListCourseMaterialsResponse con materiales y metadatos
        """
        # 1. Obtener todos los materiales del curso
        all_materials = self.repository.get_course_materials(
            course_id=request.course_id,
            access_token=request.access_token
        )
        
        # 2. Calcular conteos por tipo (antes de filtrar)
        type_counts = self._count_by_type(all_materials)
        
        # 3. Aplicar filtros
        filtered_materials = self._apply_filters(
            materials=all_materials,
            filter_type=request.filter_type,
            search_query=request.search_query
        )
        
        # 4. Aplicar límite si existe
        if request.limit:
            filtered_materials = filtered_materials[:request.limit]
        
        return ListCourseMaterialsResponse(
            materials=filtered_materials,
            total_count=len(all_materials),
            filtered_count=len(filtered_materials),
            type_counts=type_counts
        )
    
    def _apply_filters(
        self,
        materials: List[Material],
        filter_type: Optional[MaterialType],
        search_query: Optional[str]
    ) -> List[Material]:
        """
        Aplica filtros a la lista de materiales.
        
        Args:
            materials: Lista original
            filter_type: Filtrar por tipo
            search_query: Búsqueda en título/descripción
        
        Returns:
            Lista filtrada
        """
        result = materials
        
        # Filtrar por tipo principal del material
        if filter_type:
            result = [m for m in result if m.type == filter_type]
        
        # Filtrar por búsqueda (título o descripción)
        if search_query:
            query = search_query.lower()
            result = [
                m for m in result
                if query in m.title.lower()
                or (m.description and query in m.description.lower())
            ]
        
        return result
    
    def _count_by_type(self, materials: List[Material]) -> dict:
        """
        Cuenta materiales por tipo.
        
        Args:
            materials: Lista de materiales
        
        Returns:
            Dict con conteo por tipo
        """
        counts = {}
        for material in materials:
            type_name = material.type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que ListCourseMaterials funciona.
    
    Ejecutar con:
        python -m api.application.use_cases.list_course_materials
    """
    from datetime import datetime
    from src.domain.entities import Course
    from src.domain.entities.course_state import CourseState
    from src.domain.factories import MaterialFactory
    
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: ListCourseMaterials")
    print("=" * 60)
    
    # Crear Mock Repository
    class MockRepository(ClassroomRepository):
        """Mock para testing."""
        
        def get_user_courses(self, user_id: str, access_token: str):
            return []
        
        def get_course_materials(self, course_id: str, access_token: str) -> List[Material]:
            return [
                MaterialFactory.create_for_testing(
                    id="mat_1",
                    title="Guía de Integrales",
                    type=MaterialType.PDF
                ),
                MaterialFactory.create_for_testing(
                    id="mat_2",
                    title="Video Tutorial",
                    type=MaterialType.VIDEO
                ),
                MaterialFactory.create_for_testing(
                    id="mat_3",
                    title="Tarea 1",
                    type=MaterialType.ASSIGNMENT
                ),
                MaterialFactory.create_for_testing(
                    id="mat_4",
                    title="Enlace de Referencia",
                    type=MaterialType.LINK
                ),
            ]
        
        def get_course_by_id(self, course_id: str, access_token: str):
            return None
    
    mock_repo = MockRepository()
    use_case = ListCourseMaterials(mock_repo)
    
    # Test 1: Ejecutar sin filtros
    print("\n1. Ejecutar sin filtros:")
    request = ListCourseMaterialsRequest(
        course_id="course_123",
        access_token="token"
    )
    response = use_case.execute(request)
    print(f"   ✓ Total: {response.total_count}")
    print(f"   ✓ Filtrados: {response.filtered_count}")
    print(f"   ✓ Conteo por tipo: {response.type_counts}")
    
    # Test 2: Filtrar por tipo PDF
    print("\n2. Filtrar solo PDF:")
    request2 = ListCourseMaterialsRequest(
        course_id="course_123",
        access_token="token",
        filter_type=MaterialType.PDF
    )
    response2 = use_case.execute(request2)
    print(f"   ✓ Materiales PDF: {len(response2.materials)} (esperado: 1)")
    
    # Test 3: Buscar por texto
    print("\n3. Buscar 'Guía':")
    request3 = ListCourseMaterialsRequest(
        course_id="course_123",
        access_token="token",
        search_query="Guía"
    )
    response3 = use_case.execute(request3)
    print(f"   ✓ Materiales encontrados: {len(response3.materials)} (esperado: 1)")
    
    # Test 4: Aplicar límite
    print("\n4. Aplicar límite=2:")
    request4 = ListCourseMaterialsRequest(
        course_id="course_123",
        access_token="token",
        limit=2
    )
    response4 = use_case.execute(request4)
    print(f"   ✓ Materiales retornados: {len(response4.materials)} (esperado: 2)")
    
    # Test 5: Verificar DTOs
    print("\n5. Verificar DTOs:")
    print(f"   ✓ Request: course_id, access_token, filter_type, search_query, limit")
    print(f"   ✓ Response: materials, total_count, filtered_count, type_counts")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de ListCourseMaterials: OK")
    print("=" * 60)
