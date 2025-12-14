# 📄 Config — Manual Técnico

**Archivo:** `api/infrastructure/config.py`  
**Propósito:** Configuración centralizada usando variables de entorno  
**Trazabilidad:** RNF-SEG01 (Seguridad), 12-Factor App

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `os`: Acceso a variables de entorno del sistema
   - `List`: Type hints para OAUTH_SCOPES
   - POR QUÉ os.getenv: Lee variables sin exponer defaults en logs

2. **Paso 2 — Definir clase de configuración:**
   - Atributos de clase (no instancia)
   - POR QUÉ: Acceso global sin necesidad de instanciar

3. **Paso 2.1 — Variables de OAuth:**
   - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
   - `OAUTH_REDIRECT_URI`, `OAUTH_SCOPES`
   - POR QUÉ separar: Cada grupo tiene un propósito claro

4. **Paso 2.2 — Variables de aplicación:**
   - `APP_URL`, `SESSION_SECRET`, `ENVIRONMENT`
   - POR QUÉ ENVIRONMENT: Comportamiento diferente en dev/prod

5. **Paso 3 — Método validate():**
   - Verifica variables críticas al inicio
   - POR QUÉ fail-fast: Mejor fallar al arrancar que en producción

6. **Paso 4 — Métodos helper:**
   - `is_production()`, `is_development()`
   - `get_oauth_auth_url()`: Construye URL de Google OAuth

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ os: Acceso a variables de entorno del sistema
import os
from typing import List


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir clase de configuración
# ═══════════════════════════════════════════════════════════════
# POR QUÉ clase con atributos de clase: Acceso global sin instanciar
class Config:
    # ─────────────────────────────────────────────────────────
    # Paso 2.1: Variables de OAuth (sensibles)
    # ─────────────────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET', '')
    
    # ─────────────────────────────────────────────────────────
    # Paso 3: Validación al inicio
    # ─────────────────────────────────────────────────────────
    @classmethod
    def validate(cls) -> None:
        """Valida variables críticas (fail-fast)."""
        errors = []
        if not cls.GOOGLE_CLIENT_ID:
            errors.append("❌ GOOGLE_CLIENT_ID no configurado")
        if errors:
            raise ValueError("\n".join(errors))
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.infrastructure.config
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: Config
============================================================

1. Verificar variables por defecto:
   ✓ APP_URL: http://localhost:5000
   ...

✅ Prueba de Config: OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ centralizar configuración

| Beneficio | Explicación |
|-----------|-------------|
| **Un solo lugar** | Todas las variables en un archivo |
| **Fail-fast** | `validate()` detecta errores al iniciar |
| **Sin secretos en código** | Credenciales vienen de env vars |
| **12-Factor App** | Configuración externalizada |
| **Testeable** | Fácil mockear variables |

### ❌ POR QUÉ NO hardcodear o dispersar

| Problema | Ejemplo |
|----------|---------|
| **Secretos en Git** | `CLIENT_SECRET = "abc123"` es peligroso |
| **Dispersión** | Variables repartidas en muchos archivos |
| **Sin validación** | Errores aparecen en producción |
| **Inflexible** | Hay que redeploy para cambiar valores |

---

## 🎓 Conceptos Educativos

### 12-Factor App: Config

El factor III dice: "Store config in the environment"

```python
# ❌ Hardcodeado (NUNCA hacer esto)
CLIENT_ID = "mi-client-id-secreto"

# ✅ Desde variable de entorno
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
```

### Fail-Fast Principle

Validar al inicio evita errores en producción:

```python
# ✅ Fail-fast: Error inmediato al arrancar
Config.validate()

# ❌ Sin validación: Error en runtime, difícil de debuggear
# 3 horas después: "KeyError: 'GOOGLE_CLIENT_ID'"
```
