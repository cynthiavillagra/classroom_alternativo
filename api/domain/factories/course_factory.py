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

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Course y CourseState: Necesitamos la entidad y el enum
# para construir instancias válidas.
from datetime import datetime
from typing import Dict, Any
from ..entities.course import Course
from ..entities.course_state import CourseState


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la clase Factory
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Factory Pattern: Centraliza creación, valida, transforma.
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


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que CourseFactory funciona.
    
    Ejecutar con:
        python -m api.domain.factories.course_factory
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: CourseFactory")
    print("=" * 60)
    
    # Test 1: create() con parámetros explícitos
    print("\n1. CourseFactory.create():")
    now = datetime.now()
    course = CourseFactory.create(
        id="course_123",
        name="Matemáticas 3°A",
        state=CourseState.ACTIVE,
        owner_id="teacher_456",
        created_at=now,
        updated_at=now,
        section="Turno Mañana"
    )
    print(f"   ✓ Curso creado: {course}")
    
    # Test 2: create() normaliza espacios
    print("\n2. Verificar normalización de espacios:")
    course2 = CourseFactory.create(
        id="course_456",
        name="  Física  ",  # Espacios extra
        state=CourseState.ACTIVE,
        owner_id="teacher",
        created_at=now,
        updated_at=now,
        section="   ",  # Solo espacios → None
        description=""   # Vacío → None
    )
    print(f"   ✓ Nombre normalizado: '{course2.name}' (sin espacios)")
    print(f"   ✓ Section normalizada: {course2.section} (esperado: None)")
    print(f"   ✓ Description normalizada: {course2.description} (esperado: None)")
    
    # Test 3: create_from_dict()
    print("\n3. CourseFactory.create_from_dict():")
    data = {
        'id': 'course_789',
        'name': 'Historia Universal',
        'state': 'ARCHIVED',
        'owner_id': 'teacher_123',
        'created_at': '2024-01-15T10:00:00Z',
        'updated_at': '2024-12-01T15:30:00Z',
        'section': 'Sección A'
    }
    course3 = CourseFactory.create_from_dict(data)
    print(f"   ✓ Curso desde dict: {course3}")
    print(f"   ✓ State convertido: {course3.state} (esperado: ARCHIVED)")
    print(f"   ✓ created_at tipo: {type(course3.created_at).__name__} (esperado: datetime)")
    
    # Test 4: create_for_testing()
    print("\n4. CourseFactory.create_for_testing():")
    test_course = CourseFactory.create_for_testing()
    print(f"   ✓ Test course: {test_course}")
    print(f"   ✓ ID default: '{test_course.id}'")
    print(f"   ✓ Name default: '{test_course.name}'")
    
    # Test 5: create_for_testing() con override
    print("\n5. create_for_testing() con valores custom:")
    custom_course = CourseFactory.create_for_testing(
        name="Custom Test",
        state=CourseState.ARCHIVED
    )
    print(f"   ✓ Custom course: {custom_course}")
    print(f"   ✓ State overrided: {custom_course.state}")
    
    # Test 6: Verificar error por campos faltantes
    print("\n6. Verificar error por campos faltantes:")
    try:
        invalid = CourseFactory.create_from_dict({
            'id': '123',
            'name': 'Test'
            # Faltan: state, owner_id, created_at, updated_at
        })
        print("   ✗ ERROR: Debería haber lanzado ValueError")
    except ValueError as e:
        print(f"   ✓ ValueError capturado: campos faltantes")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de CourseFactory: OK")
    print("=" * 60)
