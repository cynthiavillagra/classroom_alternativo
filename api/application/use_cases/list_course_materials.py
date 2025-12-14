"""
List Course Materials Use Case - Classroom Explorer

Caso de uso para listar los materiales de un curso.
"""

from typing import List, Optional
from dataclasses import dataclass
from api.domain.entities import Material, MaterialType
from api.domain.interfaces import ClassroomRepository


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
        
        # Filtrar por tipo
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
