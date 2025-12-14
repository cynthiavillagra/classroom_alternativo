"""
Material Factory - Classroom Explorer

Factory para crear instancias de Material con validaciones y transformaciones.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from ..entities.material import Material
from ..entities.material_type import MaterialType


class MaterialFactory:
    """
    Factory para crear instancias de Material.
    
    Este factory encapsula la lógica de creación de materiales,
    permitiendo crear desde diferentes fuentes de datos.
    """
    
    @staticmethod
    def create(
        id: str,
        course_id: str,
        title: str,
        type: MaterialType,
        url: str,
        created_at: datetime,
        updated_at: datetime,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        max_points: Optional[int] = None
    ) -> Material:
        """
        Crea una instancia de Material con validaciones.
        
        Args:
            id: ID único del material
            course_id: ID del curso al que pertenece
            title: Título del material
            type: Tipo de material (enum)
            url: URL para acceder al material
            created_at: Fecha de creación
            updated_at: Última actualización
            description: Descripción (opcional)
            due_date: Fecha de entrega (opcional)
            max_points: Puntos máximos (opcional)
        
        Returns:
            Material: Instancia validada de Material
        """
        # Normalizar title
        title = title.strip() if title else ""
        
        # Normalizar description
        description = description.strip() if description else None
        if description == "":
            description = None
        
        # Normalizar URL
        url = url.strip() if url else ""
        
        # Crear la entidad
        return Material(
            id=id,
            course_id=course_id,
            title=title,
            type=type,
            url=url,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
            due_date=due_date,
            max_points=max_points
        )
    
    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> Material:
        """
        Crea una instancia de Material desde un diccionario.
        
        Args:
            data: Diccionario con los datos del material
        
        Returns:
            Material: Instancia validada de Material
        
        Raises:
            ValueError: Si faltan campos requeridos o son inválidos
        """
        # Validar campos obligatorios
        required_fields = ['id', 'course_id', 'title', 'type', 'url', 'created_at', 'updated_at']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValueError(
                f"Faltan campos obligatorios para crear Material: {', '.join(missing_fields)}"
            )
        
        # Convertir type de string a enum
        material_type = data['type']
        if isinstance(material_type, str):
            material_type = MaterialType.from_string(material_type)
        
        # Convertir fechas de string a datetime si es necesario
        created_at = data['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        
        updated_at = data['updated_at']
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
        
        # Convertir due_date si existe
        due_date = data.get('due_date')
        if due_date and isinstance(due_date, str):
            due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        
        # Crear usando el método create
        return MaterialFactory.create(
            id=data['id'],
            course_id=data['course_id'],
            title=data['title'],
            type=material_type,
            url=data['url'],
            created_at=created_at,
            updated_at=updated_at,
            description=data.get('description'),
            due_date=due_date,
            max_points=data.get('max_points')
        )
    
    @staticmethod
    def create_for_testing(
        id: str = "test_material_123",
        course_id: str = "test_course_456",
        title: str = "Test Material",
        type: MaterialType = MaterialType.PDF,
        url: str = "https://example.com/test.pdf",
        created_at: datetime = None,
        updated_at: datetime = None,
        **kwargs
    ) -> Material:
        """
        Crea una instancia de Material para testing con valores por defecto.
        
        Args:
            id: ID del material (default: "test_material_123")
            course_id: ID del curso (default: "test_course_456")
            title: Título (default: "Test Material")
            type: Tipo (default: PDF)
            url: URL (default: ejemplo válido)
            created_at: Fecha de creación (default: ahora)
            updated_at: Fecha de actualización (default: ahora)
            **kwargs: Otros parámetros opcionales
        
        Returns:
            Material: Instancia para testing
        """
        now = datetime.now()
        
        return MaterialFactory.create(
            id=id,
            course_id=course_id,
            title=title,
            type=type,
            url=url,
            created_at=created_at or now,
            updated_at=updated_at or now,
            description=kwargs.get('description'),
            due_date=kwargs.get('due_date'),
            max_points=kwargs.get('max_points')
        )
