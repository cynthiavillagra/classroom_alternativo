"""
Pytest Fixtures - Classroom Explorer

Fixtures compartidas para todos los tests.
"""
import pytest
from datetime import datetime, timezone


@pytest.fixture
def sample_course_data():
    """
    Datos de ejemplo para crear un Course.
    Vinculado a: HU-001 (Visualizar Cursos)
    """
    return {
        'id': 'course_123',
        'name': 'Matemáticas Avanzadas',
        'section': 'Sección A',
        'description': 'Curso de matemáticas',
        'state': 'ACTIVE',
        'teacher_folder': 'folder_abc',
        'creation_time': datetime.now(timezone.utc),
        'update_time': datetime.now(timezone.utc),
        'alternate_link': 'https://classroom.google.com/c/123'
    }


@pytest.fixture
def sample_material_data():
    """
    Datos de ejemplo para crear un Material.
    Vinculado a: HU-002 (Filtrar Materiales)
    """
    return {
        'id': 'material_456',
        'course_id': 'course_123',
        'title': 'Tarea de Álgebra',
        'description': 'Resolver ejercicios',
        'material_type': 'ASSIGNMENT',
        'url': 'https://docs.google.com/document/d/123',
        'max_points': 100,
        'creation_time': datetime.now(timezone.utc)
    }


@pytest.fixture
def sample_api_course():
    """
    Datos como vienen de la API de Google.
    Vinculado a: HU-003 (Mapeo de Datos)
    """
    return {
        'id': 'api_course_789',
        'name': 'Historia Universal',
        'section': 'Grupo B',
        'descriptionHeading': 'Historia',
        'courseState': 'ACTIVE',
        'creationTime': '2024-01-15T10:30:00Z',
        'updateTime': '2024-06-20T14:45:00Z',
        'alternateLink': 'https://classroom.google.com/c/789'
    }
