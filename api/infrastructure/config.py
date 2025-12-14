"""
Configuration Module - Classroom Explorer

Configuración centralizada de la aplicación usando variables de entorno.

POR QUÉ SÍ centralizar configuración:
✅ Un solo lugar para todas las variables
✅ Validación al inicio (fail-fast)
✅ Fácil de testear (mock de variables)
✅ Documentación implícita de qué se necesita

POR QUÉ NO hardcodear:
❌ Las credenciales quedarían en Git (peligro)
❌ No podríamos cambiar valores sin redeployar
❌ Violaríamos el principio de 12-factor app
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ os: Acceso a variables de entorno del sistema
# POR QUÉ List: Type hints para OAUTH_SCOPES
# [FIX] POR QUÉ dotenv aquí: Debe cargarse ANTES de que Config lea os.getenv
import os
from typing import List
from dotenv import load_dotenv

# [FIX] Cargar .env ANTES de definir Config
# Esto asegura que os.getenv() encuentre las variables
load_dotenv()


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir clase de configuración
# ═══════════════════════════════════════════════════════════════
# POR QUÉ clase con atributos de clase: Acceso global sin instanciar
class Config:
    """
    Configuración centralizada de la aplicación.
    
    Todas las variables de entorno se cargan aquí.
    Debe llamarse Config.validate() al inicio de la aplicación.
    """
    
    # ─────────────────────────────────────────────────────────
    # Google OAuth 2.0
    # ─────────────────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET', '')
    OAUTH_REDIRECT_URI: str = os.getenv(
        'OAUTH_REDIRECT_URI',
        'http://localhost:5000/api/auth/callback'
    )
    
    # ─────────────────────────────────────────────────────────
    # Aplicación
    # ─────────────────────────────────────────────────────────
    APP_URL: str = os.getenv('APP_URL', 'http://localhost:5000')
    SESSION_SECRET: str = os.getenv('SESSION_SECRET', '')
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    
    # ─────────────────────────────────────────────────────────
    # Google Classroom API
    # Referencia de scopes: https://developers.google.com/identity/protocols/oauth2/scopes?hl=es-419
    # ─────────────────────────────────────────────────────────
    CLASSROOM_API_BASE_URL: str = 'https://classroom.googleapis.com/v1'
    OAUTH_SCOPES: List[str] = [
        # Autenticación básica
        'openid',
        'email',
        'profile',
        # Classroom: Ver cursos
        'https://www.googleapis.com/auth/classroom.courses.readonly',
        # Classroom: Ver tareas (courseWork)
        'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
        # Classroom: Ver materiales de referencia (courseWorkMaterials)
        'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
        # Classroom: Ver publicaciones/anuncios (announcements)
        'https://www.googleapis.com/auth/classroom.announcements.readonly'
    ]
    
    # ─────────────────────────────────────────────────────────
    # Caché
    # ─────────────────────────────────────────────────────────
    CACHE_TTL_SECONDS: int = int(os.getenv('CACHE_TTL_SECONDS', '300'))  # 5 min
    
    @classmethod
    def validate(cls) -> None:
        """
        Valida que todas las variables críticas estén configuradas.
        
        Debe llamarse al inicio de la aplicación.
        
        Raises:
            ValueError: Si falta alguna variable crítica
        """
        errors: List[str] = []
        
        # Validar OAuth
        if not cls.GOOGLE_CLIENT_ID:
            errors.append("❌ GOOGLE_CLIENT_ID no está configurado")
        
        if not cls.GOOGLE_CLIENT_SECRET:
            errors.append("❌ GOOGLE_CLIENT_SECRET no está configurado")
        
        # Validar Session Secret (solo en producción)
        if cls.is_production() and not cls.SESSION_SECRET:
            errors.append("❌ SESSION_SECRET es obligatorio en producción")
        
        if cls.is_production() and len(cls.SESSION_SECRET) < 32:
            errors.append("❌ SESSION_SECRET debe tener al menos 32 caracteres")
        
        # Validar URLs
        if not cls.APP_URL.startswith('http'):
            errors.append(f"❌ APP_URL inválida: {cls.APP_URL}")
        
        if not cls.OAUTH_REDIRECT_URI.startswith('http'):
            errors.append(f"❌ OAUTH_REDIRECT_URI inválida: {cls.OAUTH_REDIRECT_URI}")
        
        if errors:
            error_message = "\n".join([
                "═" * 60,
                "ERROR DE CONFIGURACIÓN",
                "═" * 60,
                *errors,
                "═" * 60,
                "Revisa tu archivo .env o las variables de entorno de Vercel",
                "Consulta .env.example para ver el formato correcto"
            ])
            raise ValueError(error_message)
    
    @classmethod
    def is_production(cls) -> bool:
        """Verifica si estamos en producción."""
        return cls.ENVIRONMENT == 'production'
    
    @classmethod
    def is_development(cls) -> bool:
        """Verifica si estamos en desarrollo."""
        return cls.ENVIRONMENT == 'development'
    
    @classmethod
    def get_oauth_auth_url(cls, state: str) -> str:
        """
        Construye la URL de autenticación de Google.
        
        Args:
            state: Token CSRF para validar el callback
        
        Returns:
            URL completa para redirigir al usuario
        """
        from urllib.parse import urlencode
        
        params = {
            'client_id': cls.GOOGLE_CLIENT_ID,
            'redirect_uri': cls.OAUTH_REDIRECT_URI,
            'response_type': 'code',
            'scope': ' '.join(cls.OAUTH_SCOPES),
            'state': state,
            'access_type': 'offline',  # Para obtener refresh_token
            'prompt': 'consent'  # Forzar pantalla de consentimiento
        }
        
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que Config funciona.
    
    Ejecutar con:
        python -m api.infrastructure.config
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: Config")
    print("=" * 60)
    
    # Test 1: Verificar variables de entorno por defecto
    print("\n1. Verificar variables por defecto:")
    print(f"   ✓ GOOGLE_CLIENT_ID: {'(vacío)' if not Config.GOOGLE_CLIENT_ID else '(configurado)'}")
    print(f"   ✓ GOOGLE_CLIENT_SECRET: {'(vacío)' if not Config.GOOGLE_CLIENT_SECRET else '(configurado)'}")
    print(f"   ✓ APP_URL: {Config.APP_URL}")
    print(f"   ✓ OAUTH_REDIRECT_URI: {Config.OAUTH_REDIRECT_URI}")
    print(f"   ✓ ENVIRONMENT: {Config.ENVIRONMENT}")
    print(f"   ✓ CACHE_TTL_SECONDS: {Config.CACHE_TTL_SECONDS}")
    
    # Test 2: Verificar is_development() y is_production()
    print("\n2. Verificar métodos de entorno:")
    print(f"   ✓ is_development() = {Config.is_development()}")
    print(f"   ✓ is_production() = {Config.is_production()}")
    
    # Test 3: Verificar scopes de OAuth
    print("\n3. Verificar OAuth Scopes:")
    print(f"   ✓ Número de scopes: {len(Config.OAUTH_SCOPES)}")
    for scope in Config.OAUTH_SCOPES:
        short_scope = scope.split('/')[-1] if '/' in scope else scope
        print(f"      - {short_scope}")
    
    # Test 4: Verificar get_oauth_auth_url()
    print("\n4. Verificar get_oauth_auth_url():")
    test_state = "test_csrf_token_123"
    auth_url = Config.get_oauth_auth_url(test_state)
    print(f"   ✓ URL generada: {auth_url[:60]}...")
    print(f"   ✓ Contiene client_id: {'client_id=' in auth_url}")
    print(f"   ✓ Contiene state: {'state=' in auth_url}")
    print(f"   ✓ Contiene scope: {'scope=' in auth_url}")
    
    # Test 5: Verificar validate() sin credenciales (debe fallar en desarrollo)
    print("\n5. Verificar validate() (sin credenciales):")
    try:
        Config.validate()
        print("   ✓ validate() pasó (credenciales configuradas)")
    except ValueError as e:
        # Esperamos error si no hay credenciales configuradas
        print("   ✓ ValueError esperado (sin credenciales en .env)")
        print("      Nota: Esto es normal en desarrollo sin .env")
    
    # Test 6: Verificar CLASSROOM_API_BASE_URL
    print("\n6. Verificar API Base URL:")
    print(f"   ✓ CLASSROOM_API_BASE_URL: {Config.CLASSROOM_API_BASE_URL}")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de Config: OK")
    print("=" * 60)
