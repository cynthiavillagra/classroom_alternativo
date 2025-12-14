"""
Course State Enum - Classroom Explorer

Define los estados posibles de un curso en Google Classroom.

Basado en la documentación oficial de Google Classroom API:
https://developers.google.com/classroom/reference/rest/v1/courses#CourseState
"""

from enum import Enum


class CourseState(Enum):
    """
    Estados de un curso en Google Classroom.
    
    Estados oficiales de la API de Google:
    - ACTIVE: Curso activo y visible
    - ARCHIVED: Curso archivado (solo lectura)
    - PROVISIONED: Curso creado pero no activado
    - DECLINED: Invitación al curso rechazada
    - SUSPENDED: Curso suspendido por el administrador
    """
    
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    PROVISIONED = "PROVISIONED"
    DECLINED = "DECLINED"
    SUSPENDED = "SUSPENDED"
    
    def is_active(self) -> bool:
        """
        Verifica si el curso está activo.
        
        Returns:
            bool: True si el estado es ACTIVE
        """
        return self == CourseState.ACTIVE
    
    def is_visible(self) -> bool:
        """
        Verifica si el curso debería mostrarse por defecto.
        
        Returns:
            bool: True si el curso es ACTIVE o ARCHIVED
        """
        return self in (CourseState.ACTIVE, CourseState.ARCHIVED)
    
    def get_label(self) -> str:
        """
        Retorna la etiqueta legible para UI.
        
        Returns:
            str: Etiqueta en español
        """
        labels = {
            CourseState.ACTIVE: "Activo",
            CourseState.ARCHIVED: "Archivado",
            CourseState.PROVISIONED: "Pendiente",
            CourseState.DECLINED: "Rechazado",
            CourseState.SUSPENDED: "Suspendido"
        }
        return labels.get(self, "Desconocido")
    
    def get_color(self) -> str:
        """
        Retorna el color sugerido para UI.
        
        Returns:
            str: Color en formato hexadecimal
        """
        colors = {
            CourseState.ACTIVE: "#2ECC71",      # Verde
            CourseState.ARCHIVED: "#95A5A6",    # Gris
            CourseState.PROVISIONED: "#F39C12", # Naranja
            CourseState.DECLINED: "#E74C3C",    # Rojo
            CourseState.SUSPENDED: "#E67E22"    # Naranja oscuro
        }
        return colors.get(self, "#95A5A6")
    
    @classmethod
    def from_string(cls, value: str) -> 'CourseState':
        """
        Crea un CourseState desde un string.
        
        Args:
            value: String del estado (ej: "ACTIVE", "ARCHIVED")
        
        Returns:
            CourseState correspondiente
        
        Raises:
            ValueError: Si el estado no es válido
        """
        try:
            return cls(value.upper())
        except ValueError:
            raise ValueError(
                f"Estado de curso inválido: '{value}'. "
                f"Estados válidos: {', '.join([s.value for s in cls])}"
            )
