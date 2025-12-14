"""
Test Factories - Classroom Explorer

Pruebas simplificadas para reflejar API real.
"""
import pytest


class TestCourseFactory:
    """Tests para CourseFactory - HU-001"""
    
    def test_factory_exists(self):
        """
        Valida Criterio de Aceptación CA-001.6 de Historia HU-001.
        """
        from api.domain.factories import CourseFactory
        
        assert CourseFactory is not None
    
    def test_factory_has_create_method(self):
        """
        Valida Criterio de Aceptación CA-001.7 de Historia HU-001.
        """
        from api.domain.factories import CourseFactory
        
        assert hasattr(CourseFactory, 'create')
        assert callable(CourseFactory.create)


class TestMaterialFactory:
    """Tests para MaterialFactory - HU-002"""
    
    def test_factory_exists(self):
        """
        Valida Criterio de Aceptación CA-002.3 de Historia HU-002.
        """
        from api.domain.factories import MaterialFactory
        
        assert MaterialFactory is not None
    
    def test_factory_has_create_method(self):
        """
        Valida Criterio de Aceptación CA-002.4 de Historia HU-002.
        """
        from api.domain.factories import MaterialFactory
        
        assert hasattr(MaterialFactory, 'create')
