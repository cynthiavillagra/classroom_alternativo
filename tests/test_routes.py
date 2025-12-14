"""
Test Routes (API Handlers) - Classroom Explorer

Pruebas para los handlers HTTP.
Migradas de bloques __main__.
"""
import pytest
from http.server import BaseHTTPRequestHandler


class TestSessionStore:
    """Tests para SessionStore - HU-004"""
    
    def test_create_session(self):
        """
        Valida Criterio de Aceptación CA-004.1 de Historia HU-004.
        
        SessionStore debe crear sesiones con ID único.
        """
        from api.routes.auth import SessionStore
        
        store = SessionStore()
        session_id = store.create_session()
        
        assert session_id is not None
        assert len(session_id) > 20  # urlsafe token
    
    def test_set_and_get(self):
        """
        Valida Criterio de Aceptación CA-004.2 de Historia HU-004.
        
        SessionStore debe guardar y recuperar valores.
        """
        from api.routes.auth import SessionStore
        
        store = SessionStore()
        session_id = store.create_session()
        
        store.set(session_id, 'user_id', 'user_456')
        store.set(session_id, 'access_token', 'token_xyz')
        
        assert store.get(session_id, 'user_id') == 'user_456'
        assert store.get(session_id, 'access_token') == 'token_xyz'
    
    def test_get_invalid_session_returns_none(self):
        """
        Valida Criterio de Aceptación CA-004.3 de Historia HU-004.
        
        Sesión inexistente debe retornar None.
        """
        from api.routes.auth import SessionStore
        
        store = SessionStore()
        result = store.get('session_que_no_existe', 'key')
        
        assert result is None
    
    def test_delete_session(self):
        """
        Valida Criterio de Aceptación CA-004.4 de Historia HU-004.
        
        delete() debe eliminar la sesión (logout).
        """
        from api.routes.auth import SessionStore
        
        store = SessionStore()
        session_id = store.create_session()
        store.set(session_id, 'test_key', 'test_value')
        
        store.delete(session_id)
        
        assert store.get(session_id, 'test_key') is None


class TestAuthHandler:
    """Tests para AuthHandler - HU-004"""
    
    def test_inherits_from_base_handler(self):
        """
        Valida Criterio de Aceptación CA-004.5 de Historia HU-004.
        
        AuthHandler debe heredar de BaseHTTPRequestHandler.
        """
        from api.routes.auth import AuthHandler
        
        assert issubclass(AuthHandler, BaseHTTPRequestHandler)
    
    def test_has_do_get_method(self):
        """
        Valida Criterio de Aceptación CA-004.6 de Historia HU-004.
        
        AuthHandler debe tener método do_GET.
        """
        from api.routes.auth import AuthHandler
        
        assert hasattr(AuthHandler, 'do_GET')


class TestCoursesHandler:
    """Tests para CoursesHandler - HU-004"""
    
    def test_exists(self):
        """
        Valida Criterio de Aceptación CA-004.7 de Historia HU-004.
        
        CoursesHandler debe ser importable.
        """
        from api.routes.courses import CoursesHandler
        
        assert CoursesHandler is not None
    
    def test_inherits_correctly(self):
        """
        Valida Criterio de Aceptación CA-004.8 de Historia HU-004.
        
        CoursesHandler debe heredar de BaseHTTPRequestHandler.
        """
        from api.routes.courses import CoursesHandler
        
        assert issubclass(CoursesHandler, BaseHTTPRequestHandler)


class TestMaterialsHandler:
    """Tests para MaterialsHandler - HU-004"""
    
    def test_exists(self):
        """
        Valida Criterio de Aceptación CA-004.9 de Historia HU-004.
        
        MaterialsHandler debe ser importable.
        """
        from api.routes.materials import MaterialsHandler
        
        assert MaterialsHandler is not None
