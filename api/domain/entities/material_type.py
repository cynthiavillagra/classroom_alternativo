"""
Material Type Enum - Classroom Explorer

Define los tipos de materiales soportados por la aplicación.

POR QUÉ SÍ usar Enum:
✅ Evita strings mágicos ("pdf", "video", etc.)
✅ Autocomplete en el IDE
✅ Type safety (el IDE detecta errores)
✅ Fácil de extender (agregar nuevos tipos)

POR QUÉ NO usar strings directamente:
❌ Typos no se detectan hasta runtime
❌ No hay autocomplete
❌ Difícil de refactorizar
"""

from enum import Enum


class MaterialType(Enum):
    """
    Tipos de materiales soportados.
    
    Cada tipo tiene:
    - value: Código interno (string)
    - get_label(): Etiqueta legible para UI
    - get_icon(): Emoji/icono para UI
    """
    
    PDF = "pdf"
    VIDEO = "video"
    DOCUMENT = "document"
    LINK = "link"
    FORM = "form"
    IMAGE = "image"
    ASSIGNMENT = "assignment"
    FILE = "file"
    
    def get_label(self) -> str:
        """
        Retorna la etiqueta legible para mostrar en UI.
        
        Returns:
            str: Etiqueta en español
        """
        labels = {
            MaterialType.PDF: "PDF",
            MaterialType.VIDEO: "Video",
            MaterialType.DOCUMENT: "Documento",
            MaterialType.LINK: "Enlace",
            MaterialType.FORM: "Formulario",
            MaterialType.IMAGE: "Imagen",
            MaterialType.ASSIGNMENT: "Tarea",
            MaterialType.FILE: "Archivo"
        }
        return labels.get(self, "Desconocido")
    
    def get_icon(self) -> str:
        """
        Retorna el emoji/icono asociado al tipo.
        
        Returns:
            str: Emoji Unicode
        """
        icons = {
            MaterialType.PDF: "📄",
            MaterialType.VIDEO: "🎥",
            MaterialType.DOCUMENT: "📝",
            MaterialType.LINK: "🔗",
            MaterialType.FORM: "📋",
            MaterialType.IMAGE: "🖼️",
            MaterialType.ASSIGNMENT: "✏️",
            MaterialType.FILE: "📎"
        }
        return icons.get(self, "📎")
    
    def get_color(self) -> str:
        """
        Retorna el color sugerido para UI (hex).
        
        Returns:
            str: Color en formato hexadecimal
        """
        colors = {
            MaterialType.PDF: "#E74C3C",        # Rojo
            MaterialType.VIDEO: "#9B59B6",      # Púrpura
            MaterialType.DOCUMENT: "#3498DB",   # Azul
            MaterialType.LINK: "#1ABC9C",       # Turquesa
            MaterialType.FORM: "#F39C12",       # Naranja
            MaterialType.IMAGE: "#E67E22",      # Naranja oscuro
            MaterialType.ASSIGNMENT: "#2ECC71", # Verde
            MaterialType.FILE: "#95A5A6"        # Gris
        }
        return colors.get(self, "#95A5A6")
    
    @classmethod
    def from_string(cls, value: str) -> 'MaterialType':
        """
        Crea un MaterialType desde un string.
        
        Args:
            value: String del tipo (ej: "pdf", "video")
        
        Returns:
            MaterialType correspondiente
        
        Raises:
            ValueError: Si el tipo no es válido
        """
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(
                f"Tipo de material inválido: '{value}'. "
                f"Tipos válidos: {', '.join([t.value for t in cls])}"
            )
