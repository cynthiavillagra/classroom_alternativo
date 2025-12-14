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

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Enum: Clase base de Python para crear enumeraciones.
# Garantiza que cada valor es único y comparable.
from enum import Enum


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la enumeración de tipos de material
# ═══════════════════════════════════════════════════════════════
class MaterialType(Enum):
    """
    Tipos de materiales soportados.
    
    Cada tipo tiene:
    - value: Código interno (string)
    - get_label(): Etiqueta legible para UI
    - get_icon(): Emoji/icono para UI
    """
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Definir los valores del enum
    # ───────────────────────────────────────────────────────────
    # POR QUÉ valores en minúsculas: Consistencia con APIs REST
    # y facilita serialización JSON.
    PDF = "pdf"
    VIDEO = "video"
    DOCUMENT = "document"
    LINK = "link"
    FORM = "form"
    IMAGE = "image"
    ASSIGNMENT = "assignment"
    FILE = "file"
    ANNOUNCEMENT = "announcement"  # Publicaciones/Anuncios
    
    # ───────────────────────────────────────────────────────────
    # Paso 3: Métodos helper para UI
    # ───────────────────────────────────────────────────────────
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
            MaterialType.FILE: "Archivo",
            MaterialType.ANNOUNCEMENT: "Publicación"
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
            MaterialType.FILE: "📎",
            MaterialType.ANNOUNCEMENT: "📢"
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
            MaterialType.FILE: "#95A5A6",       # Gris
            MaterialType.ANNOUNCEMENT: "#3498DB" # Azul (publicaciones)
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


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que el enum funciona correctamente.
    
    Ejecutar con:
        python -m api.domain.entities.material_type
    
    Desde la raíz del proyecto (app classroom/)
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: MaterialType")
    print("=" * 60)
    
    # Test 1: Verificar que todos los tipos existen
    print("\n1. Verificar tipos existentes:")
    for material_type in MaterialType:
        print(f"   ✓ {material_type.name} = '{material_type.value}'")
    
    # Test 2: Verificar get_label()
    print("\n2. Verificar get_label():")
    for material_type in MaterialType:
        label = material_type.get_label()
        print(f"   ✓ {material_type.name}.get_label() = '{label}'")
    
    # Test 3: Verificar get_icon()
    print("\n3. Verificar get_icon():")
    for material_type in MaterialType:
        icon = material_type.get_icon()
        print(f"   ✓ {material_type.name}.get_icon() = {icon}")
    
    # Test 4: Verificar get_color()
    print("\n4. Verificar get_color():")
    for material_type in MaterialType:
        color = material_type.get_color()
        print(f"   ✓ {material_type.name}.get_color() = {color}")
    
    # Test 5: Verificar from_string()
    print("\n5. Verificar from_string():")
    test_values = ["pdf", "PDF", "video", "VIDEO", "document"]
    for value in test_values:
        result = MaterialType.from_string(value)
        print(f"   ✓ from_string('{value}') = {result}")
    
    # Test 6: Verificar que from_string lanza error con valor inválido
    print("\n6. Verificar error con valor inválido:")
    try:
        MaterialType.from_string("tipo_invalido")
        print("   ✗ ERROR: Debería haber lanzado ValueError")
    except ValueError as e:
        print(f"   ✓ ValueError capturado correctamente: {str(e)[:50]}...")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de MaterialType: OK")
    print("=" * 60)
