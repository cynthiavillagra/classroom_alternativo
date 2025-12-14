"""
Test Infrastructure - Classroom Explorer

Pruebas simplificadas para Config, Cache y Mapper.
"""
import pytest
import time


class TestConfig:
    """Tests para Config - HU-003"""
    
    def test_config_exists(self):
        """
        Valida Criterio de Aceptación CA-003.1 de Historia HU-003.
        """
        from api.infrastructure.config import Config
        
        assert Config is not None
    
    def test_config_has_app_url(self):
        """
        Valida Criterio de Aceptación CA-003.2 de Historia HU-003.
        """
        from api.infrastructure.config import Config
        
        assert hasattr(Config, 'APP_URL')
        assert Config.APP_URL is not None
    
    def test_config_has_environment(self):
        """
        Valida Criterio de Aceptación CA-003.3 de Historia HU-003.
        """
        from api.infrastructure.config import Config
        
        assert hasattr(Config, 'ENVIRONMENT')


class TestMemoryCache:
    """Tests para MemoryCache - HU-003"""
    
    def test_cache_exists(self):
        """
        Valida Criterio de Aceptación CA-003.4 de Historia HU-003.
        """
        from api.infrastructure.cache import MemoryCache
        
        assert MemoryCache is not None
    
    def test_cache_set_and_get(self):
        """
        Valida Criterio de Aceptación CA-003.5 de Historia HU-003.
        """
        from api.infrastructure.cache import MemoryCache
        
        cache = MemoryCache()
        cache.set('test_key', 'test_value')
        
        result = cache.get('test_key')
        assert result == 'test_value'
    
    def test_cache_get_nonexistent(self):
        """
        Valida Criterio de Aceptación CA-003.6 de Historia HU-003.
        """
        from api.infrastructure.cache import MemoryCache
        
        cache = MemoryCache()
        result = cache.get('nonexistent')
        
        assert result is None


class TestClassroomMapper:
    """Tests para ClassroomMapper - HU-003"""
    
    def test_mapper_exists(self):
        """
        Valida Criterio de Aceptación CA-003.7 de Historia HU-003.
        """
        from api.infrastructure.mappers import ClassroomMapper
        
        assert ClassroomMapper is not None
    
    def test_mapper_has_api_course_to_domain(self):
        """
        Valida Criterio de Aceptación CA-003.8 de Historia HU-003.
        """
        from api.infrastructure.mappers import ClassroomMapper
        
        assert hasattr(ClassroomMapper, 'api_course_to_domain')
