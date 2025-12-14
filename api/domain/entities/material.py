"""
Material Entity - Classroom Explorer

Entidad de dominio que representa un material de un curso de Google Classroom.

Un material puede ser: PDF, video, documento, enlace, formulario, imagen, tarea, etc.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .material_type import MaterialType


@dataclass(frozen=True)
class Material:
    """
    Entidad de dominio: Material de un curso.
    
    Esta es una entidad INMUTABLE (frozen=True).
    
    Attributes:
        id: ID único del material en Google Classroom
        course_id: ID del curso al que pertenece
        title: Título del material
        type: Tipo de material (PDF, VIDEO, etc.)
        url: URL para acceder al material
        created_at: Fecha de creación
        updated_at: Última actualización
        description: Descripción del material (opcional)
        due_date: Fecha de entrega si es tarea (opcional)
        max_points: Puntos máximos si es tarea (opcional)
    """
    
    id: str
    course_id: str
    title: str
    type: MaterialType
    url: str
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_points: Optional[int] = None
    
    def __post_init__(self):
        """
        Validaciones automáticas al crear la instancia.
        
        POR QUÉ SÍ validar aquí:
        • Garantiza que el material siempre es válido
        • Fail-fast: detecta errores inmediatamente
        • Evita propagar datos incorrectos
        """
        # Validar ID
        if not self.id or not self.id.strip():
            raise ValueError("Material ID no puede estar vacío")
        
        # Validar course_id
        if not self.course_id or not self.course_id.strip():
            raise ValueError("Material course_id no puede estar vacío")
        
        # Validar título
        if not self.title or not self.title.strip():
            raise ValueError("Material title no puede estar vacío")
        
        # Validar URL
        if not self.url or not self.url.strip():
            raise ValueError("Material URL no puede estar vacío")
        
        if not self.url.startswith(('http://', 'https://')):
            raise ValueError(
                f"Material URL debe comenzar con http:// o https://, "
                f"recibido: '{self.url}'"
            )
        
        # Validar que updated_at >= created_at
        if self.updated_at < self.created_at:
            raise ValueError(
                f"updated_at ({self.updated_at}) no puede ser anterior a "
                f"created_at ({self.created_at})"
            )
        
        # Validar due_date si existe
        if self.due_date and self.due_date < self.created_at:
            raise ValueError(
                f"due_date ({self.due_date}) no puede ser anterior a "
                f"created_at ({self.created_at})"
            )
        
        # Validar max_points si existe
        if self.max_points is not None and self.max_points < 0:
            raise ValueError(
                f"max_points no puede ser negativo, recibido: {self.max_points}"
            )
    
    def is_assignment(self) -> bool:
        """
        Verifica si el material es una tarea (assignment).
        
        Returns:
            bool: True si es una tarea
        
        Example:
            >>> material = Material(type=MaterialType.ASSIGNMENT, ...)
            >>> material.is_assignment()
            True
        """
        return self.type == MaterialType.ASSIGNMENT
    
    def has_due_date(self) -> bool:
        """
        Verifica si el material tiene fecha de entrega.
        
        Returns:
            bool: True si tiene due_date
        """
        return self.due_date is not None
    
    def is_overdue(self) -> bool:
        """
        Verifica si el material está vencido (pasó la fecha de entrega).
        
        Returns:
            bool: True si está vencido
        
        Example:
            >>> material = Material(due_date=datetime(2024, 1, 1), ...)
            >>> material.is_overdue()  # Si hoy es después del 1 de enero
            True
        """
        if not self.has_due_date():
            return False
        
        return datetime.now() > self.due_date
    
    def days_until_due(self) -> Optional[int]:
        """
        Calcula cuántos días faltan para la fecha de entrega.
        
        Returns:
            int: Días hasta la entrega (negativo si ya pasó)
            None: Si no tiene fecha de entrega
        
        Example:
            >>> material.days_until_due()
            5  # Faltan 5 días
        """
        if not self.has_due_date():
            return None
        
        delta = self.due_date - datetime.now()
        return delta.days
    
    def get_type_label(self) -> str:
        """
        Obtiene la etiqueta legible del tipo de material.
        
        Returns:
            str: Etiqueta en español (ej: "PDF", "Video")
        """
        return self.type.get_label()
    
    def get_type_icon(self) -> str:
        """
        Obtiene el icono del tipo de material.
        
        Returns:
            str: Emoji del tipo (ej: "📄", "🎥")
        """
        return self.type.get_icon()
    
    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (para serialización JSON).
        
        Returns:
            dict: Representación en diccionario de la entidad
        
        Example:
            >>> material.to_dict()
            {
                'id': '789012',
                'title': 'Guía de Integrales',
                'type': 'pdf',
                'url': 'https://drive.google.com/...',
                ...
            }
        """
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'type': self.type.value,  # Convertir enum a string
            'type_label': self.get_type_label(),
            'type_icon': self.get_type_icon(),
            'url': self.url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'max_points': self.max_points,
            'is_assignment': self.is_assignment(),
            'has_due_date': self.has_due_date(),
            'is_overdue': self.is_overdue(),
            'days_until_due': self.days_until_due()
        }
    
    def __str__(self) -> str:
        """
        Representación legible para humanos.
        
        Returns:
            str: Descripción del material
        
        Example:
            >>> print(material)
            Material: Guía de Integrales (PDF) - https://drive.google.com/...
        """
        return (
            f"Material: {self.title} ({self.get_type_label()}) - {self.url}"
        )
    
    def __repr__(self) -> str:
        """
        Representación para debugging.
        
        Returns:
            str: Representación técnica del material
        
        Example:
            >>> material
            Material(id='789012', title='Guía de Integrales', type=MaterialType.PDF)
        """
        return (
            f"Material(id='{self.id}', title='{self.title}', "
            f"type={self.type}, course_id='{self.course_id}')"
        )
