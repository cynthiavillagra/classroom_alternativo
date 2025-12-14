# Manual Técnico: .env.example

## Propósito

**Trazabilidad Completa:**
* **Módulo:** Configuración de Entorno
* **Historia de Usuario:** HU-000 (Setup del proyecto)
* **Criterio de Aceptación:** CA-000.1 (Las credenciales están documentadas y seguras)

---

## Estrategia de Construcción Incremental

1. **Validación de Dependencias:** 
   - Este archivo NO tiene dependencias, es el segundo archivo del proyecto
   - POR QUÉ segundo: Después de requirements.txt, necesitamos definir las variables de entorno

2. **Estructura Base:**
   - Formato `.env` (key=value)
   - Comentarios explicativos con `#`
   - Placeholders `<...>` para valores sensibles

3. **Lógica Nuclear:**
   - NUNCA valores reales (Regla de Oro #1: ZERO-TRUST)
   - Cada variable documentada con su propósito
   - Instrucciones de cómo obtener los valores

---

## Aclaración Metodológica

Este archivo NO tiene bloque `if __name__ == "__main__"` porque:
- Es un archivo de configuración, no código Python
- Se valida mediante: ¿existe .env con valores reales?

---

## Código Fuente

```env
# ══════════════════════════════════════════════════════════════
# Classroom Explorer - Variables de Entorno
# ══════════════════════════════════════════════════════════════

# 🔐 Google OAuth 2.0
GOOGLE_CLIENT_ID=<TU_CLIENT_ID_DE_GOOGLE>
GOOGLE_CLIENT_SECRET=<TU_CLIENT_SECRET_DE_GOOGLE>

# 🌐 URLs de la Aplicación
APP_URL=http://localhost:5000
OAUTH_REDIRECT_URI=http://localhost:5000/api/auth/callback

# 🔑 Secreto para Sesiones
SESSION_SECRET=<GENERA_UN_SECRET_ALEATORIO>

# 🧪 Entorno
ENVIRONMENT=development
```

---

## Prueba de Fuego

1. Verifica que el archivo existe:
```powershell
Test-Path .env.example
```

2. Verifica que NO contiene valores reales:
```powershell
Select-String -Path .env.example -Pattern "GOCSPX" | Measure-Object
# Esperado: Count = 0 (no hay secretos reales)
```

---

## Análisis Dual

### Por qué SÍ:
- **Seguridad:** Los valores reales van en `.env` (ignorado por Git)
- **Documentación:** Nuevos desarrolladores saben qué variables configurar
- **Portabilidad:** Cualquiera puede replicar el proyecto

### Por qué NO (sin .env.example):
- **Secretos expuestos:** Si ponemos valores en el código
- **Onboarding difícil:** Nadie sabe qué variables necesita
- **Errores en producción:** Faltan variables y la app crashea
