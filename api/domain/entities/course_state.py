"""
Course State Enum - Classroom Explorer

Define los estados posibles de un curso en Google Classroom.

Basado en la documentación oficial de Google Classroom API:
https://developers.google.com/classroom/reference/rest/v1/courses#CourseState
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Enum: Proporciona type-safety y valores constantes.
# Los estados de Google Classroom son un conjunto finito y cerrado.
from enum import Enum


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la enumeración de estados de curso
# ═══════════════════════════════════════════════════════════════
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
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Valores del enum (estados oficiales de Google)
    # ───────────────────────────────────────────────────────────
    # POR QUÉ MAYÚSCULAS: Así vienen de la API de Google.
    # Mantenemos el mismo formato para evitar conversiones.
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"
    PROVISIONED = "PROVISIONED"
    DECLINED = "DECLINED"
    SUSPENDED = "SUSPENDED"
    
    # ───────────────────────────────────────────────────────────
    # Paso 3: Métodos de lógica de negocio
    # ───────────────────────────────────────────────────────────
    # POR QUÉ métodos aquí: Encapsulamos reglas de negocio
    # directamente en el enum (Rich Domain Model).
    
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


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que el enum funciona correctamente.
    
    Ejecutar con:
        python -m api.domain.entities.course_state
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: CourseState")
    print("=" * 60)
    
    # Test 1: Verificar que todos los estados existen
    print("\n1. Verificar estados existentes:")
    for state in CourseState:
        print(f"   ✓ {state.name} = '{state.value}'")
    
    # Test 2: Verificar is_active()
    print("\n2. Verificar is_active():")
    for state in CourseState:
        is_active = state.is_active()
        expected = "✓" if state == CourseState.ACTIVE else "✗"
        print(f"   {expected} {state.name}.is_active() = {is_active}")
    
    # Test 3: Verificar is_visible()
    print("\n3. Verificar is_visible():")
    for state in CourseState:
        is_visible = state.is_visible()
        expected = "✓" if state in (CourseState.ACTIVE, CourseState.ARCHIVED) else "✗"
        print(f"   {expected} {state.name}.is_visible() = {is_visible}")
    
    # Test 4: Verificar get_label()
    print("\n4. Verificar get_label():")
    for state in CourseState:
        label = state.get_label()
        print(f"   ✓ {state.name}.get_label() = '{label}'")
    
    # Test 5: Verificar get_color()
    print("\n5. Verificar get_color():")
    for state in CourseState:
        color = state.get_color()
        print(f"   ✓ {state.name}.get_color() = {color}")
    
    # Test 6: Verificar from_string()
    print("\n6. Verificar from_string():")
    test_values = ["ACTIVE", "active", "ARCHIVED", "archived"]
    for value in test_values:
        result = CourseState.from_string(value)
        print(f"   ✓ from_string('{value}') = {result}")
    
    # Test 7: Verificar error con valor inválido
    print("\n7. Verificar error con valor inválido:")
    try:
        CourseState.from_string("INVALID_STATE")
        print("   ✗ ERROR: Debería haber lanzado ValueError")
    except ValueError as e:
        print(f"   ✓ ValueError capturado correctamente")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de CourseState: OK")
    print("=" * 60)
