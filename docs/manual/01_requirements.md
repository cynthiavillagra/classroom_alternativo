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

## 📦 Estrategia de Construcción Incremental

1. **Paso 1 — Identificar dependencias core:** Flask para web, requests para HTTP
2. **Paso 2 — Agregar seguridad:** PyJWT para tokens, cryptography para encriptación
3. **Paso 3 — Integrar Google:** google-auth y google-auth-oauthlib para OAuth
4. **Paso 4 — Validación:** pydantic para type safety en runtime
5. **Paso 5 — Utilidades:** python-dotenv para variables de entorno
6. **Paso 6 — Testing:** pytest y plugins para pruebas automatizadas

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
# Desde la raíz del proyecto (app classroom/)
pip install -r requirements.txt
pip list | findstr flask
```

### Salida Esperada
```
Flask                 3.0.0
```

### Verificación Completa
```powershell
python -c "import flask; import jwt; import requests; print('✅ Todas las dependencias OK')"
```

### Salida Esperada
```
✅ Todas las dependencias OK
```

---

## 🎓 Aclaración Metodológica

Este archivo NO tiene bloque `if __name__ == "__main__"` porque es un archivo de configuración, no código Python ejecutable. La "Prueba de Fuego" se realiza verificando que `pip install` funciona correctamente.
