"""
Material Entity - Classroom Explorer

Entidad de dominio que representa un material de un curso de Google Classroom.

Un material puede ser: PDF, video, documento, enlace, formulario, imagen, tarea, etc.
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ dataclass: Reduce boilerplate para entidades
# POR QUÉ MaterialType: Enum para type-safety en tipos de material
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .material_type import MaterialType


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la entidad Material
# ═══════════════════════════════════════════════════════════════
# POR QUÉ frozen=True: Inmutabilidad garantiza consistencia
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
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Campos requeridos
    # ───────────────────────────────────────────────────────────
    # POR QUÉ type: MaterialType: Usa enum para type-safety
    id: str
    course_id: str
    title: str
    type: MaterialType
    url: str
    created_at: datetime
    updated_at: datetime
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.2: Campos opcionales (específicos de tareas)
    # ───────────────────────────────────────────────────────────
    # POR QUÉ separados: Solo aplican si el material es ASSIGNMENT
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_points: Optional[int] = None
    
    # ───────────────────────────────────────────────────────────
    # Paso 3: Validaciones en __post_init__
    # ───────────────────────────────────────────────────────────
    # POR QUÉ: Fail-fast, garantiza datos válidos desde la creación
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
        
        # [FIX] Usar datetime con timezone para comparar con due_date que tiene timezone
        from datetime import timezone
        now = datetime.now(timezone.utc)
        # Si due_date no tiene timezone, asumir UTC
        due = self.due_date
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        return now > due
    
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
        
        # [FIX] Usar datetime con timezone
        from datetime import timezone
        now = datetime.now(timezone.utc)
        due = self.due_date
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        delta = due - now
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


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que la entidad Material funciona.
    
    Ejecutar con:
        python -m api.domain.entities.material
    """
    from datetime import timedelta
    
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: Material")
    print("=" * 60)
    
    # Test 1: Crear un material válido (PDF)
    print("\n1. Crear material válido (PDF):")
    now = datetime.now()
    material = Material(
        id="mat_123",
        course_id="course_456",
        title="Guía de Integrales",
        type=MaterialType.PDF,
        url="https://drive.google.com/file123",
        created_at=now,
        updated_at=now,
        description="Guía completa de integrales"
    )
    print(f"   ✓ Material creado: {material}")
    
    # Test 2: Verificar is_assignment()
    print("\n2. Verificar is_assignment():")
    print(f"   ✓ PDF.is_assignment() = {material.is_assignment()} (esperado: False)")
    
    # Test 3: Crear una tarea con due_date
    print("\n3. Crear tarea con due_date:")
    future_date = now + timedelta(days=5)
    assignment = Material(
        id="task_789",
        course_id="course_456",
        title="Tarea 1: Ejercicios",
        type=MaterialType.ASSIGNMENT,
        url="https://classroom.google.com/task",
        created_at=now,
        updated_at=now,
        due_date=future_date,
        max_points=100
    )
    print(f"   ✓ Tarea creada: {assignment}")
    print(f"   ✓ is_assignment() = {assignment.is_assignment()} (esperado: True)")
    print(f"   ✓ has_due_date() = {assignment.has_due_date()} (esperado: True)")
    print(f"   ✓ is_overdue() = {assignment.is_overdue()} (esperado: False)")
    print(f"   ✓ days_until_due() = {assignment.days_until_due()} (esperado: ~5)")
    
    # Test 4: Verificar get_type_label() y get_type_icon()
    print("\n4. Verificar tipo label e icon:")
    print(f"   ✓ PDF: {material.get_type_icon()} {material.get_type_label()}")
    print(f"   ✓ Assignment: {assignment.get_type_icon()} {assignment.get_type_label()}")
    
    # Test 5: Verificar to_dict()
    print("\n5. Verificar to_dict():")
    mat_dict = material.to_dict()
    print(f"   ✓ to_dict() tiene {len(mat_dict)} campos")
    print(f"      - type: {mat_dict['type']}")
    print(f"      - type_label: {mat_dict['type_label']}")
    print(f"      - type_icon: {mat_dict['type_icon']}")
    
    # Test 6: Verificar validación de URL inválida
    print("\n6. Verificar validación de URL inválida:")
    try:
        invalid = Material(
            id="test",
            course_id="course",
            title="Test",
            type=MaterialType.LINK,
            url="google.com",  # Sin http://
            created_at=now,
            updated_at=now
        )
        print("   ✗ ERROR: Debería haber lanzado ValueError")
    except ValueError as e:
        print(f"   ✓ ValueError capturado: URL inválida")
    
    # Test 7: Verificar validación de max_points negativo
    print("\n7. Verificar validación de max_points negativo:")
    try:
        invalid = Material(
            id="test",
            course_id="course",
            title="Test",
            type=MaterialType.ASSIGNMENT,
            url="https://test.com",
            created_at=now,
            updated_at=now,
            max_points=-10
        )
        print("   ✗ ERROR: Debería haber lanzado ValueError")
    except ValueError as e:
        print(f"   ✓ ValueError capturado: max_points negativo")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de Material: OK")
    print("=" * 60)
