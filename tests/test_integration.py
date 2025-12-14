"""
Test Integration (Main Server) - Classroom Explorer

Pruebas de integración para el servidor y VercelBridge.
Migradas del bloque __main__ de main.py.
"""
import pytest
from http.server import BaseHTTPRequestHandler
import sys


class TestMainRouter:
    """Tests para MainRouter - HU-000"""
    
    def test_mainrouter_exists(self):
        """
        Valida Criterio de Aceptación CA-000.1 de Historia HU-000.
        
        MainRouter debe ser importable.
        """
        from main import MainRouter
        
        assert MainRouter is not None
    
    def test_inherits_base_http_handler(self):
        """
        Valida Criterio de Aceptación CA-000.2 de Historia HU-000.
        
        MainRouter debe heredar de BaseHTTPRequestHandler.
        """
        from main import MainRouter
        
        assert issubclass(MainRouter, BaseHTTPRequestHandler)
    
    def test_has_do_get(self):
        """
        Valida Criterio de Aceptación CA-000.3 de Historia HU-000.
        
        MainRouter debe implementar do_GET.
        """
        from main import MainRouter
        
        assert hasattr(MainRouter, 'do_GET')


class TestVercelBridge:
    """Tests para VercelBridge - HU-000"""
    
    def test_vercel_bridge_exists(self):
        """
        Valida Criterio de Aceptación CA-000.4 de Historia HU-000.
        
        VercelBridge debe ser importable.
        """
        from main import VercelBridge
        
        assert VercelBridge is not None
    
    def test_vercel_bridge_callable(self):
        """
        Valida Criterio de Aceptación CA-000.5 de Historia HU-000.
        
        VercelBridge debe ser callable (WSGI).
        """
        from main import VercelBridge
        
        bridge = VercelBridge()
        assert callable(bridge)
    
    def test_app_variable_exposed(self):
        """
        Valida Criterio de Aceptación CA-000.6 de Historia HU-000.
        
        Variable 'app' debe estar expuesta para Vercel.
        """
        from main import app
        
        assert app is not None
        assert callable(app)


class TestEnvironmentDiagnostics:
    """Tests para Diagnóstico de Entorno - HU-000"""
    
    def test_diagnose_function_exists(self):
        """
        Valida Criterio de Aceptación CA-000.7 de Historia HU-000.
        
        Debe existir función de diagnóstico.
        """
        from main import _diagnose_environment
        
        assert callable(_diagnose_environment)
    
    def test_diagnose_returns_list(self):
        """
        Valida Criterio de Aceptación CA-000.8 de Historia HU-000.
        
        Diagnóstico debe retornar lista de warnings.
        """
        from main import _diagnose_environment
        
        result = _diagnose_environment()
        assert isinstance(result, list)


class TestPythonPurity:
    """Tests para verificar Python POO puro - HU-000"""
    
    def test_no_flask_loaded(self):
        """
        Valida Criterio de Aceptación CA-000.9 de Historia HU-000.
        
        Flask NO debe estar cargado (Python POO puro).
        """
        # Importar main para cargar todo
        import main
        
        assert 'flask' not in sys.modules
    
    def test_no_fastapi_loaded(self):
        """
        Valida Criterio de Aceptación CA-000.10 de Historia HU-000.
        
        FastAPI NO debe estar cargado.
        """
        import main
        
        assert 'fastapi' not in sys.modules
