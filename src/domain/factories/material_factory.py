"""
Material Factory - Classroom Explorer

Factory para crear instancias de Material con validaciones y transformaciones.
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Material y MaterialType: Entidad y enum para type-safety
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from ..entities.material import Material
from ..entities.material_type import MaterialType


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la clase Factory
# ═══════════════════════════════════════════════════════════════
# POR QUÉ similar a CourseFactory: Consistencia en patrones
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
        max_points: Optional[int] = None,
        attachments: Tuple[Dict[str, Any], ...] = ()
    ) -> Material:
        """
        Crea una instancia de Material con validaciones.
        
        Args:
            id: ID único del material
            course_id: ID del curso al que pertenece
            title: Título del material
            type: Tipo de material (enum)
            url: URL para acceder al material (principal)
            created_at: Fecha de creación
            updated_at: Última actualización
            description: Descripción (opcional)
            due_date: Fecha de entrega (opcional)
            max_points: Puntos máximos (opcional)
            attachments: Tupla de adjuntos [{type, title, url}, ...]
        
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
            max_points=max_points,
            attachments=tuple(attachments) if attachments else ()
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
            max_points=data.get('max_points'),
            attachments=tuple(data.get('attachments', []))
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


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que MaterialFactory funciona.
    
    Ejecutar con:
        python -m api.domain.factories.material_factory
    """
    from datetime import timedelta
    
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: MaterialFactory")
    print("=" * 60)
    
    # Test 1: create() con parámetros explícitos
    print("\n1. MaterialFactory.create():")
    now = datetime.now()
    material = MaterialFactory.create(
        id="mat_123",
        course_id="course_456",
        title="Guía de Integrales",
        type=MaterialType.PDF,
        url="https://drive.google.com/file123",
        created_at=now,
        updated_at=now
    )
    print(f"   ✓ Material creado: {material}")
    
    # Test 2: create() normaliza espacios
    print("\n2. Verificar normalización:")
    material2 = MaterialFactory.create(
        id="mat_456",
        course_id="course_789",
        title="  Video Tutorial  ",  # Espacios
        type=MaterialType.VIDEO,
        url="  https://youtube.com/watch  ",  # Espacios
        created_at=now,
        updated_at=now,
        description=""  # Vacío → None
    )
    print(f"   ✓ Title normalizado: '{material2.title}'")
    print(f"   ✓ URL normalizada: '{material2.url}'")
    print(f"   ✓ Description: {material2.description} (esperado: None)")
    
    # Test 3: create_from_dict()
    print("\n3. MaterialFactory.create_from_dict():")
    data = {
        'id': 'mat_789',
        'course_id': 'course_123',
        'title': 'Tarea 1',
        'type': 'assignment',
        'url': 'https://classroom.google.com/task',
        'created_at': '2024-01-15T10:00:00Z',
        'updated_at': '2024-12-01T15:30:00Z',
        'due_date': '2024-12-20T23:59:00Z',
        'max_points': 100
    }
    material3 = MaterialFactory.create_from_dict(data)
    print(f"   ✓ Material desde dict: {material3}")
    print(f"   ✓ Type convertido: {material3.type}")
    print(f"   ✓ due_date tipo: {type(material3.due_date).__name__}")
    print(f"   ✓ max_points: {material3.max_points}")
    
    # Test 4: create_for_testing()
    print("\n4. MaterialFactory.create_for_testing():")
    test_mat = MaterialFactory.create_for_testing()
    print(f"   ✓ Test material: {test_mat}")
    print(f"   ✓ ID default: '{test_mat.id}'")
    print(f"   ✓ Type default: {test_mat.type}")
    
    # Test 5: create_for_testing() con override
    print("\n5. create_for_testing() con valores custom:")
    custom_mat = MaterialFactory.create_for_testing(
        title="Custom Video",
        type=MaterialType.VIDEO,
        due_date=now + timedelta(days=7),
        max_points=50
    )
    print(f"   ✓ Custom material: {custom_mat}")
    print(f"   ✓ Type overrided: {custom_mat.type}")
    print(f"   ✓ has_due_date: {custom_mat.has_due_date()}")
    
    # Test 6: Verificar error por campos faltantes
    print("\n6. Verificar error por campos faltantes:")
    try:
        invalid = MaterialFactory.create_from_dict({
            'id': '123',
            'title': 'Test'
            # Faltan: course_id, type, url, created_at, updated_at
        })
        print("   ✗ ERROR: Debería haber lanzado ValueError")
    except ValueError as e:
        print(f"   ✓ ValueError capturado: campos faltantes")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de MaterialFactory: OK")
    print("=" * 60)
