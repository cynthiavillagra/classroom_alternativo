"""
Course Entity - Classroom Explorer

Entidad de dominio que representa un curso de Google Classroom.

POR QUÉ SÍ usar dataclass:
✅ Menos boilerplate (no necesitas __init__, __repr__, etc.)
✅ Inmutabilidad con frozen=True
✅ Type hints integrados
✅ Generación automática de __eq__, __hash__

POR QUÉ NO usar dict:
❌ No hay validación de tipos
❌ No hay autocomplete
❌ Fácil cometer errores (typos en keys)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .course_state import CourseState


@dataclass(frozen=True)
class Course:
    """
    Entidad de dominio: Curso de Google Classroom.
    
    Esta es una entidad INMUTABLE (frozen=True).
    Una vez creada, no se puede modificar.
    
    POR QUÉ SÍ inmutabilidad:
    • Previene bugs (nadie puede cambiar el estado por accidente)
    • Thread-safe (seguro en concurrencia)
    • Más fácil de razonar sobre el código
    • Permite usar como key en diccionarios
    
    Attributes:
        id: ID único del curso en Google Classroom
        name: Nombre del curso (ej: "Matemáticas 3°A")
        section: Sección o división (opcional)
        description: Descripción del curso (opcional)
        state: Estado del curso (ACTIVE, ARCHIVED, etc.)
        owner_id: ID del profesor propietario
        created_at: Fecha de creación en Classroom
        updated_at: Última actualización
    """
    
    id: str
    name: str
    state: CourseState
    owner_id: str
    created_at: datetime
    updated_at: datetime
    section: Optional[str] = None
    description: Optional[str] = None
    
    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear la instancia.
        
        POR QUÉ SÍ validar en __post_init__:
        • Fail-fast: Detectamos errores inmediatamente
        • Garantiza que la entidad siempre es válida
        • Evita estados inconsistentes
        
        POR QUÉ NO validar en el constructor:
        • Con frozen=True, no podemos modificar después de __init__
        • __post_init__ es el lugar correcto en dataclasses
        """
        # Validar que el ID no esté vacío
        if not self.id or not self.id.strip():
            raise ValueError("Course ID no puede estar vacío")
        
        # Validar que el nombre tenga al menos 3 caracteres
        if not self.name or len(self.name.strip()) < 3:
            raise ValueError(
                f"Course name debe tener al menos 3 caracteres, recibido: '{self.name}'"
            )
        
        # Validar que owner_id no esté vacío
        if not self.owner_id or not self.owner_id.strip():
            raise ValueError("Course owner_id no puede estar vacío")
        
        # Validar que updated_at >= created_at
        if self.updated_at < self.created_at:
            raise ValueError(
                f"updated_at ({self.updated_at}) no puede ser anterior a "
                f"created_at ({self.created_at})"
            )
    
    def is_active(self) -> bool:
        """
        Verifica si el curso está activo.
        
        Returns:
            bool: True si el estado es ACTIVE
        
        Example:
            >>> course = Course(...)
            >>> if course.is_active():
            ...     print("El curso está activo")
        """
        return self.state.is_active()
    
    def is_visible(self) -> bool:
        """
        Verifica si el curso debería mostrarse en la UI.
        
        Un curso es visible si está ACTIVE o ARCHIVED.
        Los cursos PROVISIONED, DECLINED o SUSPENDED no se muestran.
        
        Returns:
            bool: True si el curso es visible
        """
        return self.state.is_visible()
    
    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (para serialización JSON).
        
        POR QUÉ SÍ este método:
        • Necesitamos enviar la entidad al frontend como JSON
        • Controlamos exactamente qué campos se exponen
        • Podemos formatear fechas, enums, etc.
        
        Returns:
            dict: Representación en diccionario de la entidad
        
        Example:
            >>> course.to_dict()
            {
                'id': '123456',
                'name': 'Matemáticas 3°A',
                'state': 'ACTIVE',
                ...
            }
        """
        return {
            'id': self.id,
            'name': self.name,
            'section': self.section,
            'description': self.description,
            'state': self.state.value,  # Convertir enum a string
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),  # ISO 8601
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active(),
            'is_visible': self.is_visible()
        }
    
    def __str__(self) -> str:
        """
        Representación legible para humanos.
        
        Returns:
            str: Descripción del curso
        
        Example:
            >>> print(course)
            Course: Matemáticas 3°A (ACTIVE)
        """
        section_str = f" - {self.section}" if self.section else ""
        return f"Course: {self.name}{section_str} ({self.state.value})"
    
    def __repr__(self) -> str:
        """
        Representación para debugging.
        
        Returns:
            str: Representación técnica del curso
        
        Example:
            >>> course
            Course(id='123456', name='Matemáticas 3°A', state=CourseState.ACTIVE)
        """
        return (
            f"Course(id='{self.id}', name='{self.name}', "
            f"state={self.state}, owner_id='{self.owner_id}')"
        )
