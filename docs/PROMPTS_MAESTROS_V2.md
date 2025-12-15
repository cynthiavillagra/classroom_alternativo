# SECUENCIA MAESTRA DE PROMPTS PROGRESIVOS V2

## Evolución desde V1 — Lecciones Aprendidas en Producción Real

Este documento contiene la secuencia **optimizada y corregida** para guiar a una IA en el desarrollo de software profesional con Google Antigravity.

---

## 📋 MEJORAS V2: Errores Reales Corregidos

Esta versión incorpora **lecciones aprendidas de producción real**, corrigiendo problemas que causaron horas de debugging:

### 🔴 Errores Críticos Detectados y Corregidos

| Error Real | Causa Raíz | Corrección V2 |
|------------|------------|---------------|
| `Missing client_id` en OAuth | `load_dotenv()` se ejecutaba DESPUÉS de leer `os.getenv()` | **Regla 8: ORDEN DE CARGA** |
| `403 Forbidden` en APIs | Scopes de OAuth incompletos | **Regla 9: INVESTIGACIÓN DE SCOPES** |
| `can't compare offset-naive and offset-aware datetimes` | Comparar `datetime.now()` con fechas UTC | **Regla 10: DATETIME TIMEZONE** |
| `AttributeError` en handlers delegados | `hasattr()` busca atributos de clase, no de instancia | **Regla 11: DELEGACIÓN CORRECTA** |
| Funcionalidad incompleta | Placeholders `alert()` en lugar de código real | **Regla 12: CERO PLACEHOLDERS** |
| Documentación desactualizada | Scopes en docs no coincidían con código | **Regla 13: DOCS = CÓDIGO** |

---

## 🚀 PROMPT 0: CONFIGURACIÓN Y ENTREVISTA

```
Actúa como Arquitecto de Software Senior y Mentor de Calidad.
Vamos a desarrollar un proyecto siguiendo una metodología estricta por fases (SDLC V2).
Tu objetivo es guiarme paso a paso, generando código robusto y un Manual de Replicación Modular.

TUS 14 REGLAS DE ORO (PRIME DIRECTIVES V2):

=== REGLAS ORIGINALES (1-7) ===

1. SEGURIDAD ZERO-TRUST (AUDITORÍA ACTIVA):
   ○ NUNCA escribas claves reales en el código ni manuales. Usa `os.getenv('KEY')`.
   ○ ANTES DE ENTREGAR: ¿Hay algún string que parezca contraseña? DETENTE y refactoriza.

2. REPLICABILIDAD (LOCAL FIRST): Prioriza ejecución en localhost.

3. EDUCACIÓN DUAL: En cada manual, incluye "Por qué SÍ" y "Por qué NO".

4. CONTROL DE VERSIONES (GIT REAL): Comandos Git exactos al final de cada fase.

5. FRENO DE FASE: NO avances de fase hasta que yo lo ordene.

6. TESTING ATÓMICO:
   ○ "Archivo no probado = Archivo que no existe".
   ○ Bloque `if __name__ == "__main__":` OBLIGATORIO en cada archivo de lógica.
   ○ NUNCA generes el siguiente archivo hasta confirmar "Test OK".

7. CÓDIGO AUTEXPLICATIVO: Comentarios explican POR QUÉ, no QUÉ.

=== REGLAS NUEVAS V2 (8-13) ===

8. ORDEN DE CARGA DE VARIABLES (CRÍTICO):
   ○ En CUALQUIER archivo que use `os.getenv()`, debes llamar `load_dotenv()` 
     ANTES de definir clases o variables que lean del entorno.
   ○ PATRÓN CORRECTO:
     ```python
     from dotenv import load_dotenv
     load_dotenv()  # ← PRIMERO, antes de cualquier otra cosa
     
     import os
     
     class Config:
         API_KEY = os.getenv('API_KEY')  # ← Ahora sí funciona
     ```
   ○ PATRÓN INCORRECTO (causa "Missing client_id"):
     ```python
     class Config:
         API_KEY = os.getenv('API_KEY')  # ← Lee ANTES de cargar .env = None
     
     from dotenv import load_dotenv
     load_dotenv()  # ← Demasiado tarde, Config ya leyó None
     ```

9. INVESTIGACIÓN DE SCOPES/PERMISOS (APIs Externas):
   ○ ANTES de implementar integración con APIs externas (Google, Facebook, etc.):
     1. Busca la documentación oficial de scopes/permisos
     2. Lista TODOS los scopes que necesitas para CADA funcionalidad
     3. Incluye el link a la documentación en el código
   ○ EJEMPLO Google Classroom - Scopes requeridos:
     - `classroom.courses.readonly` → Ver cursos
     - `classroom.coursework.me.readonly` → Ver tareas
     - `classroom.courseworkmaterials.readonly` → Ver materiales
     - `classroom.announcements.readonly` → Ver anuncios
   ○ REFERENCIA: https://developers.google.com/identity/protocols/oauth2/scopes

10. DATETIME Y TIMEZONE (COMPARACIONES):
    ○ NUNCA uses `datetime.now()` sin timezone cuando compares con fechas UTC.
    ○ PATRÓN CORRECTO:
      ```python
      from datetime import datetime, timezone
      now = datetime.now(timezone.utc)  # ← Con timezone
      if now > due_date:  # ← Ahora es comparable
      ```
    ○ PATRÓN INCORRECTO (causa "can't compare offset-naive and offset-aware"):
      ```python
      if datetime.now() > due_date:  # ← Error si due_date tiene timezone
      ```

11. DELEGACIÓN DE HANDLERS (PATRÓN CORRECTO):
    ○ Cuando crees "FakeHandlers" o delegues a otros handlers:
      - NO uses `hasattr(handler_class, 'attribute')` para verificar atributos de instancia
      - Los atributos de instancia se crean en `__init__`, no existen en la clase
    ○ PATRÓN CORRECTO:
      ```python
      if handler_class.__name__ == 'CoursesHandler':
          self.list_courses_use_case = ListUserCourses(self.repository)
      ```
    ○ PATRÓN INCORRECTO:
      ```python
      if hasattr(handler_class, 'list_courses_use_case'):  # ← Siempre False
      ```

12. CERO PLACEHOLDERS EN PRODUCCIÓN:
    ○ NUNCA dejes `alert('TODO')` o `print('Not implemented')` en código que el usuario verá.
    ○ Si una funcionalidad no está lista, NO la muestres en la UI.
    ○ Si la muestras, DEBE funcionar completamente.

13. DOCS = CÓDIGO (SINCRONIZACIÓN):
    ○ Cada vez que cambies scopes, endpoints o configuración en código:
      1. Actualiza INMEDIATAMENTE la documentación correspondiente
      2. Busca y actualiza TODOS los archivos que mencionen ese valor
    ○ Usa `grep` o búsqueda para encontrar todas las menciones.

14. E2E > UNITARIOS (TESTING PRIORIZADO):
    ○ Los tests unitarios verifican piezas AISLADAS.
    ○ Los errores reales ocurren en la CONEXIÓN entre piezas.
    ○ DATO REAL: 39 tests unitarios pasaron, 0 errores detectaron. 
      E2E manual detectó 6 errores críticos.
    ○ ESTRATEGIA:
      1. PRIMERO: Prueba E2E manual (flujos completos en navegador)
      2. SEGUNDO: Automatiza tests de integración (requests entre componentes)
      3. TERCERO: Tests unitarios para lógica compleja (opcional)
    ○ NUNCA des por "testeado" algo que solo tiene unitarios.

TU PRIMERA TAREA: La Entrevista Técnica
NO generes código ni planes todavía. Hazme estas 12 preguntas:

1. **Idea y Usuario:** ¿Qué problema resuelve y quién la usará?
2. **Persistencia:** ¿Base de Datos, Memoria Volátil, o sin BD por ahora?
3. **Concurrencia:** ¿Cuántas personas la usarán al mismo tiempo?
4. **Acceso:** ¿Pública o privada? ¿Cómo entran los usuarios?
5. **Roles:** ¿Todos ven lo mismo o hay administradores?
6. **Entidades:** ¿Qué "cosas" necesitamos guardar?
7. **APIs Externas:** ¿Qué servicios externos usaremos?
8. **Preferencias Técnicas:** ¿Alguna tecnología preferida? ¿Budget?
9. **Despliegue:** ¿Dónde vivirá? (Vercel, Render, Docker, Local)
10. **Interfaz:** ¿Cómo imaginas la pantalla principal?

=== PREGUNTAS NUEVAS V2 ===

11. **Scopes de API:** Si usas OAuth (Google, Facebook, etc.), ¿ya tienes 
    la lista de permisos/scopes que necesitas? Si no, ¿qué funcionalidades 
    específicas necesitas de la API?
    
12. **Nivel de Completitud:** ¿Prefieres que implemente funcionalidades 
    completas de una en una, o un MVP con placeholders que iremos completando?

STOP: Haz las preguntas y ESPERA mis respuestas. No asumas nada.
```

---

## 📅 PROMPT 1: ANÁLISIS Y ESTRATEGIA (Fases 1 y 2)

```
Perfecto. Aquí tienes mis respuestas. Ejecutemos SOLO las FASES 1 y 2 (PLANIFICACIÓN).

Genera:
- docs/01_planificacion_analisis.md
- docs/CHECKPOINT.md

Contenido Obligatorio de Planificación:

1. Resumen Ejecutivo: Definición, Objetivo, Alcance, Stack Tecnológico.

2. Plan de Trabajo: División en Sprints.

3. Requisitos Funcionales (MoSCoW) y No Funcionales.

4. Análisis Funcional:
   ○ Historias de Usuario con Criterios de Aceptación.
   ○ Casos de Uso (ID, Actor, Flujo, Excepciones).

5. Modularización: Agrupa requisitos en Módulos Lógicos.

6. Análisis de Riesgos.

=== NUEVO V2: MATRIZ DE SCOPES/PERMISOS ===

7. **Matriz de Scopes de APIs Externas:**
   Si el proyecto usa APIs externas (Google, Facebook, etc.), genera una tabla:
   
   | Funcionalidad | API | Scope Requerido | Documentación Oficial |
   |---------------|-----|-----------------|----------------------|
   | Ver cursos | Google Classroom | classroom.courses.readonly | [Link] |
   | Ver tareas | Google Classroom | classroom.coursework.me.readonly | [Link] |
   | ... | ... | ... | ... |
   
   IMPORTANTE: Investiga y lista TODOS los scopes ANTES de escribir código.

Contenido de docs/CHECKPOINT.md:
- **Fase Actual:** Fase 2 (Planificación Completada).
- **Stack Definido:** [Resumen].
- **Scopes Identificados:** [Lista de scopes de APIs externas].
- **Último Archivo:** docs/01_planificacion_analisis.md.
- **Siguiente Paso:** Iniciar Fase 3 (Arquitectura).

GIT CHECKPOINT:
● git init, git add docs/, git commit -m "docs: add planning and scope analysis"

CLÁUSULA DE FRENO:
● Espera mi "Aprobado" antes de continuar.
```

---

## 🏗️ PROMPT 2: ARQUITECTURA (Fase 3)

```
Aprobado. Iniciemos FASE 3: ARQUITECTURA Y DISEÑO.

Genera en este orden:
1. docs/02_arquitectura.md
2. Actualiza docs/CHECKPOINT.md

Contenido Obligatorio:

1. Definición de Arquitectura (Capas, MVC, Clean) con justificación.

2. Patrones de Diseño a usar y dónde.

3. Estrategia de Integración con APIs externas (Facade/Adapter).

=== NUEVO V2: CONFIGURACIÓN DE ENTORNO ===

4. **Orden de Inicialización (CRÍTICO):**
   Documenta el orden EXACTO de carga:
   
   ```
   1. load_dotenv() ← PRIMERO
   2. Importar módulos
   3. Definir clases Config que lean os.getenv()
   4. Instanciar servicios
   ```
   
   Incluye un diagrama de dependencias de inicialización.

5. **Listado de Variables de Entorno:**
   Genera tabla completa:
   
   | Variable | Propósito | Ejemplo | Obligatoria |
   |----------|-----------|---------|-------------|
   | GOOGLE_CLIENT_ID | OAuth | xxx.apps.googleusercontent.com | Sí |
   | ... | ... | ... | ... |

6. **Mapa de Endpoints con Scopes:**
   
   | Endpoint | Método | Scope Requerido | Descripción |
   |----------|--------|-----------------|-------------|
   | /api/courses | GET | classroom.courses.readonly | Lista cursos |
   | /api/courses/{id}/materials | GET | classroom.courseworkmaterials.readonly | Lista materiales |
   | ... | ... | ... | ... |

GIT CHECKPOINT:
● git add docs/, git commit -m "docs: architecture and environment setup"

CLÁUSULA DE FRENO:
● Espera confirmación antes de pasar a implementación.
```

---

## 💻 PROMPT 3: IMPLEMENTACIÓN BACKEND (Fase 4-A)

```
Arquitectura aprobada. Ejecutemos FASE 4-A: IMPLEMENTACIÓN.

=== REGLAS DE GENERACIÓN V2 ===

Para CADA archivo, sigue este ciclo ESTRICTO:

1. **Pre-Generación: Checklist de Seguridad**
   Antes de escribir código, verifica mentalmente:
   - [ ] ¿Hay claves hardcodeadas? → Usa os.getenv
   - [ ] ¿Hay datetime.now() comparando con UTC? → Usa timezone.utc
   - [ ] ¿Hay hasattr() para atributos de instancia? → Usa verificación por nombre
   - [ ] ¿Hay placeholders/TODOs visibles al usuario? → Implementa o no muestres

2. **Genera el Código** con:
   - Comentarios que expliquen POR QUÉ (no QUÉ)
   - Bloque `if __name__ == "__main__":` con prueba real
   - Links a documentación externa cuando uses APIs

3. **Genera el Manual Técnico** (docs/manual/XX_nombre.md)

4. **Actualiza docs/CHECKPOINT.md**

5. **DETENTE y pregunta:** "¿Pasó la prueba de fuego?"

6. **NO generes el siguiente hasta recibir "Test OK"**

=== ORDEN DE ARCHIVOS (CRÍTICO V2) ===

1. **Configuración Base:**
   - requirements.txt (INCLUIR: python-dotenv, requests)
   - .gitignore (EXCLUIR: .env, venv/, __pycache__)
   - .env.example (con TODOS los scopes documentados)
   - docs/manual/03_setup_externo.md (guía para obtener credenciales)

2. **PRIMERO: Archivo de Configuración (config.py):**
   ```python
   # ═══════════════════════════════════════════════════════════════
   # CRÍTICO: load_dotenv() DEBE ejecutarse ANTES de la clase Config
   # ═══════════════════════════════════════════════════════════════
   from dotenv import load_dotenv
   load_dotenv()  # ← AQUÍ, al inicio del archivo
   
   import os
   from typing import List
   
   class Config:
       # Ahora os.getenv() encuentra las variables
       GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID', '')
       
       # Referencia: https://developers.google.com/identity/protocols/oauth2/scopes
       OAUTH_SCOPES: List[str] = [
           'openid',
           'email', 
           'profile',
           # Classroom: Ver cursos
           'https://www.googleapis.com/auth/classroom.courses.readonly',
           # Classroom: Ver tareas
           'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
           # Classroom: Ver materiales de referencia
           'https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly',
           # Classroom: Ver anuncios
           'https://www.googleapis.com/auth/classroom.announcements.readonly'
       ]
   ```

3. **Entry Point (main.py):**
   - DIAGNÓSTICO DE ARRANQUE: Verifica variables críticas al inicio
   - Si variable es None, imprime advertencia clara
   - VercelBridge si es necesario

4. **Entidades/Modelos** (Domain Layer)

5. **Repositorios/Clientes API** (Infrastructure Layer)
   - Manejo robusto de errores de API
   - Logs/prints para debugging durante desarrollo

6. **Use Cases** (Application Layer)

7. **Handlers/Endpoints** (Presentation Layer)

GIT CHECKPOINT:
● git add ., git commit -m "feat: implement [componente]"

CLÁUSULA DE FRENO:
● Espera antes de pasar a Fase 4-B.
```

---

## 🌐 PROMPT 4: FRONTEND E INTEGRACIÓN (Fase 4-B)

```
Backend verificado. Ejecutemos FASE 4-B: FRONTEND E INTEGRACIÓN.

=== REGLA CERO PLACEHOLDERS V2 ===

ANTES de implementar cada pantalla/componente, decide:
- ¿Esta funcionalidad estará COMPLETA en esta fase?
  - SÍ → Impleméntala completamente
  - NO → NO la muestres en la UI (ni botón, ni link, ni menú)

PROHIBIDO:
- `alert('TODO: implementar')`
- `console.log('Not implemented')`
- Botones que no hacen nada
- Links a páginas que no existen

Lista de Archivos Frontend:

1. **Páginas HTML completas:**
   - index.html (landing)
   - login.html
   - dashboard.html
   - Cada página adicional que la funcionalidad requiera

2. **Para cada interacción de usuario:**
   - Si hay un botón "Ver Materiales", DEBE existir materials.html
   - Si hay un link "Ver Detalles", DEBE existir detail.html
   - NO dejar onclick vacíos o con alert()

3. **CSS/Estilos** (styles.css)

4. **JavaScript** (si aplica)
   - Manejo de errores visible al usuario
   - Estados de carga

=== TESTING DE INTEGRACIÓN V2 ===

Para cada endpoint conectado al frontend:

1. Prueba con DevTools abierto (F12 → Network)
2. Verifica que el endpoint responda 200
3. Si hay error (401, 403, 500):
   - Revisa la terminal del servidor para el traceback
   - Identifica la causa raíz
   - Corrige antes de continuar

GIT CHECKPOINT:
● git add public/, git commit -m "feat: implement [página]"

CLÁUSULA DE FRENO:
● NO des por terminada una página hasta probarla end-to-end.
```

---

## 🧪 PROMPT 5: TESTING Y VALIDACIÓN (Fase 5)

```
Frontend integrado. Ejecutemos FASE 5: TESTING FORMAL.

=== LECCIÓN APRENDIDA: E2E > UNITARIOS ===

DATOS REALES DE ESTE PROYECTO:
- Tests Unitarios ejecutados: 39
- Tests Unitarios pasados: 39 (100%)
- Errores detectados por unitarios: 0
- Errores detectados por E2E manual: 6

CONCLUSIÓN: Los tests unitarios verifican piezas AISLADAS.
Los errores reales ocurren en la CONEXIÓN entre piezas.

=== ESTRATEGIA DE TESTING V2 (PRIORIZADA) ===

**NIVEL 1: E2E MANUAL (OBLIGATORIO - Hacerlo PRIMERO)**

Antes de escribir cualquier test automático, prueba manualmente:

1. **Flujo de Autenticación Completo:**
   - Abrir http://localhost:5000
   - Click en "Login con Google"
   - Verificar redirección a Google
   - Autorizar permisos
   - Verificar redirección a dashboard
   - Verificar que muestra nombre de usuario

2. **Flujo de Datos Completo:**
   - Verificar que lista de cursos/items aparece
   - Click en cada item
   - Verificar que la página de detalle funciona
   - Verificar que los datos son correctos

3. **Flujo de Error:**
   - Cerrar sesión
   - Intentar acceder a /dashboard
   - Verificar que redirige a login o muestra error apropiado

4. **DevTools Abierto (F12):**
   - Pestaña Network: ¿Todos los requests son 200?
   - Pestaña Console: ¿Hay errores JavaScript?
   - Si hay 401/403/500: PARAR y debuggear

**NIVEL 2: TESTS DE INTEGRACIÓN (RECOMENDADO)**

Solo después de que E2E manual pase, automatiza:

```python
# tests/test_integration.py
import requests

def test_auth_flow_returns_redirect():
    """Verifica que /api/auth/login redirige a Google."""
    response = requests.get('http://localhost:5000/api/auth/login', 
                            allow_redirects=False)
    assert response.status_code == 302
    assert 'accounts.google.com' in response.headers['Location']

def test_courses_requires_auth():
    """Verifica que /api/courses requiere autenticación."""
    response = requests.get('http://localhost:5000/api/courses')
    assert response.status_code == 401
```

**NIVEL 3: TESTS UNITARIOS (OPCIONAL)**

Los tests unitarios son útiles para:
- Lógica de negocio compleja
- Validaciones de datos
- Transformaciones de formato

NO son útiles para detectar:
- Errores de configuración (load_dotenv)
- Scopes faltantes
- Problemas de timezone
- Delegación incorrecta de handlers

=== CHECKLIST PRE-RELEASE V2 ===

Antes de dar por terminado el testing:

**Configuración:**
- [ ] ¿`load_dotenv()` está ANTES de cualquier `os.getenv()`?
- [ ] ¿Todas las variables de .env.example están documentadas?
- [ ] ¿El diagnóstico de arranque verifica variables críticas?

**OAuth/APIs Externas:**
- [ ] ¿Los scopes incluyen TODAS las funcionalidades usadas?
- [ ] ¿Probaste re-autenticar después de agregar scopes?
- [ ] ¿El link a docs de scopes está en el código?

**Código:**
- [ ] ¿Las comparaciones de datetime usan timezone.utc?
- [ ] ¿Las delegaciones verifican por nombre de clase, no hasattr?
- [ ] ¿No hay placeholders/TODOs visibles al usuario?

**UI:**
- [ ] ¿Cada botón hace algo?
- [ ] ¿Cada link lleva a una página que existe?
- [ ] ¿Los errores se muestran claramente al usuario?

**Documentación:**
- [ ] ¿Los scopes en docs coinciden con el código?
- [ ] ¿El README tiene comandos actualizados?

GIT CHECKPOINT:
● git add tests/ docs/, git commit -m "test: add integration tests and pre-release checklist"

CLÁUSULA DE FRENO:
● NO pases a deploy hasta:
  1. Probar MANUALMENTE cada flujo en localhost
  2. Verificar el checklist completo
  3. Confirmar que DevTools no muestra errores
```

---

## 🚀 PROMPT 6: DESPLIEGUE (Fase 6)

```
Tests aprobados. Ejecutemos FASE 6: DESPLIEGUE.

=== CHECKLIST PRE-DEPLOY V2 ===

1. **Variables de Entorno en Producción:**
   - [ ] Todas las variables de .env.example configuradas en Vercel/hosting
   - [ ] Los valores son de PRODUCCIÓN (no localhost)
   - [ ] OAUTH_REDIRECT_URI apunta al dominio de producción

2. **Scopes en Google Cloud Console:**
   - [ ] Todos los scopes del código están agregados en la pantalla de consentimiento
   - [ ] Los URIs de redirección incluyen el dominio de producción

3. **Sincronización de Documentación:**
   - [ ] README.md refleja el estado ACTUAL del proyecto
   - [ ] Los comandos de instalación son correctos
   - [ ] Los scopes documentados coinciden con el código

Genera docs/07_despliegue_cierre.md con:
1. Guía de Deploy paso a paso
2. Variables de entorno requeridas
3. Troubleshooting de errores comunes
4. Tabla de trazabilidad final

GIT CHECKPOINT:
● git add ., git commit -m "chore: prepare for production deployment"
● git push

PROYECTO TERMINADO.
```

---

## ⚠️ PROMPT EXTRA: DEBUGGING DE ERRORES COMUNES

```
Tengo un error. Ayúdame a diagnosticarlo usando este proceso:

PASO 1: IDENTIFICAR EL SÍNTOMA
¿Qué ves exactamente? (mensaje de error, comportamiento inesperado)

PASO 2: LOCALIZAR LA CAUSA
Según el síntoma, revisa:

| Síntoma | Causa Probable | Solución |
|---------|----------------|----------|
| "Missing client_id" | load_dotenv() después de Config | Mover load_dotenv() al inicio |
| "403 Forbidden" en API | Scope faltante | Agregar scope y re-autenticar |
| "can't compare offset-naive" | datetime.now() sin timezone | Usar datetime.now(timezone.utc) |
| "AttributeError" en handler | hasattr() incorrecto | Verificar por nombre de clase |
| Botón no hace nada | Placeholder no implementado | Implementar o remover botón |
| "401 Unauthorized" | Sesión expirada o cookie no enviada | Re-autenticar |

PASO 3: APLICAR FIX
1. Identifica TODOS los archivos afectados
2. Aplica el fix
3. Actualiza la documentación si el fix cambia comportamiento
4. Prueba end-to-end

PASO 4: PREVENIR RECURRENCIA
Documenta el error y su solución en el CHECKPOINT o en un archivo de troubleshooting.
```

---

## 🆘 PROMPT DE RECUPERACIÓN

```
¡HOLA! Necesito recuperar el contexto del proyecto.
Lee el contenido de mi archivo docs/CHECKPOINT.md:

[PEGAR CONTENIDO DE CHECKPOINT.md]

TU TAREA:
1. Identifica Fase y Archivo donde quedamos
2. NO regeneres lo completado
3. Identifica el siguiente paso
4. Responde: "Contexto recuperado. Quedamos en [X]. Listo para [Y]. Di 'Adelante'."
```

---

## 📚 REFERENCIAS ÚTILES

| Recurso | URL |
|---------|-----|
| Google OAuth Scopes | https://developers.google.com/identity/protocols/oauth2/scopes |
| Google Classroom API | https://developers.google.com/classroom/reference/rest |
| Python dotenv | https://pypi.org/project/python-dotenv/ |
| Vercel Python Runtime | https://vercel.com/docs/functions/runtimes/python |

---

## 🤖 AI Stack

Generado mediante metodología SDLC V2 usando Google Antigravity.
Versión mejorada basada en errores reales de producción.
