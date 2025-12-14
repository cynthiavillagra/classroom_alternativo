"""
Course Factory - Classroom Explorer

Factory para crear instancias de Course con validaciones y transformaciones.

POR QUÉ SÍ usar Factory Pattern:
✅ Centraliza la lógica de creación
✅ Valida y transforma datos antes de crear la entidad
✅ Facilita crear desde diferentes fuentes (dict, API, etc.)
✅ Permite agregar lógica de creación sin modificar la entidad

POR QUÉ NO crear directamente:
❌ Course(...) requiere pasar todos los parámetros
❌ No hay validación previa
❌ Difícil crear desde diccionarios (API responses)
"""

from datetime import datetime
from typing import Dict, Any
from ..entities.course import Course
from ..entities.course_state import CourseState


class CourseFactory:
    """
    Factory para crear instancias de Course.
    
    Este factory encapsula la lógica de creación de cursos,
    permitiendo crear desde diferentes fuentes de datos.
    
    Example:
        >>> # Crear desde diccionario (API response)
        >>> data = {
        ...     'id': '123456',
        ...     'name': 'Matemáticas 3°A',
        ...     'state': 'ACTIVE',
        ...     'ownerId': '987654',
        ...     'creationTime': '2024-01-15T10:00:00Z',
        ...     'updateTime': '2024-12-01T15:30:00Z'
        ... }
        >>> course = CourseFactory.create_from_dict(data)
    """
    
    @staticmethod
    def create(
        id: str,
        name: str,
        state: CourseState,
        owner_id: str,
        created_at: datetime,
        updated_at: datetime,
        section: str = None,
        description: str = None
    ) -> Course:
        """
        Crea una instancia de Course con validaciones.
        
        Args:
            id: ID único del curso
            name: Nombre del curso
            state: Estado del curso
            owner_id: ID del profesor propietario
            created_at: Fecha de creación
            updated_at: Última actualización
            section: Sección (opcional)
            description: Descripción (opcional)
        
        Returns:
            Course: Instancia validada de Course
        
        Raises:
            ValueError: Si algún parámetro es inválido
        """
        # Validaciones adicionales antes de crear
        # (Las validaciones básicas están en Course.__post_init__)
        
        # Normalizar name (quitar espacios extra)
        name = name.strip() if name else ""
        
        # Normalizar section
        section = section.strip() if section else None
        if section == "":
            section = None
        
        # Normalizar description
        description = description.strip() if description else None
        if description == "":
            description = None
        
        # Crear la entidad
        return Course(
            id=id,
            name=name,
            state=state,
            owner_id=owner_id,
            created_at=created_at,
            updated_at=updated_at,
            section=section,
            description=description
        )
    
    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> Course:
        """
        Crea una instancia de Course desde un diccionario.
        
        Este método es útil para crear cursos desde respuestas de API
        que vienen como diccionarios JSON.
        
        Args:
            data: Diccionario con los datos del curso
        
        Returns:
            Course: Instancia validada de Course
        
        Raises:
            ValueError: Si faltan campos requeridos o son inválidos
            KeyError: Si falta un campo obligatorio
        
        Example:
            >>> data = {'id': '123', 'name': 'Math', 'state': 'ACTIVE', ...}
            >>> course = CourseFactory.create_from_dict(data)
        """
        # Validar que existan los campos obligatorios
        required_fields = ['id', 'name', 'state', 'owner_id', 'created_at', 'updated_at']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValueError(
                f"Faltan campos obligatorios para crear Course: {', '.join(missing_fields)}"
            )
        
        # Convertir state de string a enum
        state = data['state']
        if isinstance(state, str):
            state = CourseState.from_string(state)
        
        # Convertir fechas de string a datetime si es necesario
        created_at = data['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        
        updated_at = data['updated_at']
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
        
        # Crear usando el método create
        return CourseFactory.create(
            id=data['id'],
            name=data['name'],
            state=state,
            owner_id=data['owner_id'],
            created_at=created_at,
            updated_at=updated_at,
            section=data.get('section'),
            description=data.get('description')
        )
    
    @staticmethod
    def create_for_testing(
        id: str = "test_course_123",
        name: str = "Test Course",
        state: CourseState = CourseState.ACTIVE,
        owner_id: str = "test_owner_456",
        created_at: datetime = None,
        updated_at: datetime = None,
        **kwargs
    ) -> Course:
        """
        Crea una instancia de Course para testing con valores por defecto.
        
        Este método facilita la creación de cursos en tests,
        proporcionando valores por defecto razonables.
        
        Args:
            id: ID del curso (default: "test_course_123")
            name: Nombre del curso (default: "Test Course")
            state: Estado (default: ACTIVE)
            owner_id: ID del owner (default: "test_owner_456")
            created_at: Fecha de creación (default: ahora)
            updated_at: Fecha de actualización (default: ahora)
            **kwargs: Otros parámetros opcionales
        
        Returns:
            Course: Instancia para testing
        
        Example:
            >>> # Test con valores por defecto
            >>> course = CourseFactory.create_for_testing()
            
            >>> # Test con valores personalizados
            >>> course = CourseFactory.create_for_testing(
            ...     name="Custom Test Course",
            ...     state=CourseState.ARCHIVED
            ... )
        """
        now = datetime.now()
        
        return CourseFactory.create(
            id=id,
            name=name,
            state=state,
            owner_id=owner_id,
            created_at=created_at or now,
            updated_at=updated_at or now,
            section=kwargs.get('section'),
            description=kwargs.get('description')
        )
