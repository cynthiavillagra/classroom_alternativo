# 📄 requirements.txt — Manual Técnico

**Archivo:** `requirements.txt`  
**Propósito:** Define todas las dependencias Python del proyecto  
**Trazabilidad:** RNF-MANT04 (Convenciones de código), Setup inicial

---

## 📝 Contenido

```txt
# Framework Web
flask==3.0.0
werkzeug==3.0.1

# Autenticación y Seguridad
PyJWT==2.8.0
cryptography==41.0.7

# HTTP Client
requests==2.31.0
google-auth==2.25.2
google-auth-oauthlib==1.2.0

# Validación de Datos
pydantic==2.5.3

# Utilidades
python-dotenv==1.0.0

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
```

---

## ✅ POR QUÉ SÍ estas dependencias

| Dependencia | Justificación |
|-------------|---------------|
| **Flask** | Framework web ligero, compatible con Vercel Serverless, no tiene overhead de Django |
| **PyJWT** | Estándar de la industria para JWT, simple y seguro |
| **requests** | Cliente HTTP más usado en Python, simple y confiable |
| **google-auth** | Librería oficial de Google, maneja OAuth 2.0 correctamente |
| **pydantic** | Validación de datos con type hints, previene errores en runtime |
| **python-dotenv** | Carga variables de .env automáticamente en desarrollo |
| **pytest** | Framework de testing más popular en Python |

---

## ❌ POR QUÉ NO otras alternativas

| Alternativa | Por Qué NO |
|-------------|------------|
| **Django** | Demasiado pesado para serverless, tiene ORM que no necesitamos |
| **FastAPI** | Excelente, pero más complejo para aprender (async/await) |
| **urllib** | Más bajo nivel que requests, menos legible |
| **jose** (JWT) | Menos mantenido que PyJWT |
| **httpx** | Más moderno pero requests es más estable y conocido |

---

## 🎓 CONCEPTOS EDUCATIVOS

### ¿Qué es requirements.txt?
- Es el estándar de Python para declarar dependencias
- Similar a `package.json` en Node.js
- Permite reproducir el entorno exacto en cualquier máquina

### ¿Por qué versiones fijas (==)?
- ✅ **Reproducibilidad**: Todos instalan las mismas versiones
- ✅ **Estabilidad**: Evita que updates rompan el código
- ❌ **Trade-off**: No obtenemos bugfixes automáticos

**Alternativa:** Usar `~=` para permitir parches (ej: `flask~=3.0.0` permite 3.0.1, 3.0.2, pero no 3.1.0)

---

## 📦 Instalación

```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar (Windows)
.\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar
pip list
```
