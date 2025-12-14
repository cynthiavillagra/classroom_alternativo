# Manual Técnico: setup_externo.md

## Propósito

**Trazabilidad Completa:**
* **Módulo:** Configuración de Entorno
* **Historia de Usuario:** HU-000 (Setup del proyecto)
* **Criterio de Aceptación:** CA-000.2 (El desarrollador puede obtener credenciales siguiendo la guía)

---

## Estrategia de Construcción Incremental

1. **Validación de Dependencias:** 
   - Depende de: `.env.example` (debe existir primero)
   - POR QUÉ tercero: Después de definir qué variables necesitamos, explicamos cómo obtenerlas

2. **Estructura Base:**
   - Guía paso a paso con capturas mentales
   - Cada paso numerado y verificable
   - Solución de problemas al final

3. **Lógica Nuclear:**
   - Instrucciones para Google Cloud Console
   - Configuración de OAuth 2.0
   - Scopes necesarios para Classroom API

---

## Aclaración Metodológica

Este archivo NO tiene bloque `if __name__ == "__main__"` porque:
- Es documentación Markdown, no código
- Se valida mediante: ¿el usuario pudo obtener las credenciales?

---

## Contenido del Archivo

El archivo `docs/setup_externo.md` contiene:

1. **Prerrequisitos** — Qué necesitas antes de empezar
2. **Paso 1** — Crear proyecto en Google Cloud Console
3. **Paso 2** — Habilitar APIs (Classroom, OAuth)
4. **Paso 3** — Crear credenciales OAuth 2.0
5. **Paso 4** — Configurar .env
6. **Paso 5** — Verificar configuración
7. **Solución de Problemas** — Errores comunes

---

## Prueba de Fuego

1. Sigue los pasos del archivo
2. Verifica que puedas iniciar sesión con Google
3. Esperado: Redirigido a dashboard tras login

---

## Análisis Dual

### Por qué SÍ:
- **Autocontenido:** Cualquiera puede configurar sin preguntar
- **Educativo:** Enseña sobre OAuth 2.0
- **Replicable:** El proyecto funciona desde cero

### Por qué NO (sin guía):
- **Bloqueo:** Desarrolladores no saben cómo empezar
- **Soporte constante:** Todos preguntan lo mismo
- **Proyecto abandonado:** Muy difícil de configurar
