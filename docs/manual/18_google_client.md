# 📄 GoogleClassroomClient — Manual Técnico

**Archivo:** `api/infrastructure/google_classroom_client.py`  
**Propósito:** Cliente HTTP Singleton para Google Classroom API  
**Trazabilidad:** RF-M02/M03 (Listar cursos/materiales), Integración API

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `requests`: Librería HTTP estándar, simple y robusta
   - `time`: Para retry con backoff exponencial
   - `Config`: URL base de la API
   - POR QUÉ requests: Más legible que urllib, bien mantenida

2. **Paso 2 — Implementar Singleton:**
   - `_instance`: Variable de clase para única instancia
   - `__new__()`: Crea o retorna la instancia existente
   - POR QUÉ Singleton: Reutiliza sesión HTTP, evita overhead

3. **Paso 2.1 — Inicialización:**
   - `_initialized`: Flag para inicializar solo una vez
   - `_session`: Sesión HTTP reutilizable
   - POR QUÉ Session: Conexiones persistentes, más rápido

4. **Paso 3 — Método `_make_request()`:**
   - Headers con Authorization Bearer
   - Retry con backoff exponencial (1s, 2s, 4s)
   - Manejo de errores (429 rate limit, 5xx server errors)
   - POR QUÉ retry: APIs externas pueden fallar temporalmente

5. **Paso 4 — Métodos públicos de API:**
   - `list_courses()`: GET /courses
   - `get_course()`: GET /courses/{id}
   - `list_course_work()`: GET /courses/{id}/courseWork
   - `list_course_work_materials()`: GET /courses/{id}/courseWorkMaterials

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema. NO hace llamadas reales a la API.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
import requests
import time
from typing import Dict, Any, Optional
from .config import Config


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir la clase Cliente (Singleton)
# ═══════════════════════════════════════════════════════════════
class GoogleClassroomClient:
    _instance: Optional['GoogleClassroomClient'] = None
    
    # ───────────────────────────────────────────────────────────
    # Paso 2.1: Singleton con __new__
    # ───────────────────────────────────────────────────────────
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    # ───────────────────────────────────────────────────────────
    # Paso 3: Request con retry
    # ───────────────────────────────────────────────────────────
    def _make_request(self, endpoint, access_token, ...):
        headers = {"Authorization": f"Bearer {access_token}"}
        for attempt in range(max_retries):
            try:
                response = self._session.get(url, headers=headers)
                if response.status_code == 429:  # Rate limit
                    time.sleep(2 ** attempt)  # Backoff exponencial
                    continue
                return response.json()
            except Exception:
                time.sleep(2 ** attempt)
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.infrastructure.google_classroom_client
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: GoogleClassroomClient
============================================================

1. Verificar Singleton:
   ✓ Tipo: GoogleClassroomClient
   ✓ Es la misma instancia: True
   ...

⚠️  NOTA: No se hicieron llamadas reales a Google API
✅ Prueba de GoogleClassroomClient: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ Singleton para HTTP Client

| Beneficio | Explicación |
|-----------|-------------|
| **Conexiones persistentes** | Session reutiliza conexiones TCP |
| **Menos overhead** | No crea cliente nuevo en cada request |
| **Rate limiting central** | Un lugar para controlar throttling |
| **Retry centralizado** | Lógica de retry en un solo lugar |

### ❌ POR QUÉ NO una instancia por request

| Problema | Impacto |
|----------|---------|
| **Overhead** | Crear sesión HTTP es costoso |
| **Sin reutilización** | Nueva conexión TCP cada vez |
| **Lento** | Handshake TLS repetido |
| **Difícil de gestionar** | Rate limiting disperso |

---

## 🎓 Conceptos Educativos

### Singleton Pattern con __new__

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Siempre retorna la misma instancia
a = Singleton()
b = Singleton()
assert a is b  # True
```

### Backoff Exponencial

Cuando la API falla, esperamos cada vez más:
- Intento 1: espera 1 segundo (2⁰)
- Intento 2: espera 2 segundos (2¹)
- Intento 3: espera 4 segundos (2²)

Esto evita saturar una API que está teniendo problemas.
