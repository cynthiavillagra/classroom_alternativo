SECUENCIA MAESTRA DE PROMPTS PROGRESIVOS(Con Freno de Fase, Git Flow, Seguridad Zero-Trust, Testing Atómico Incremental y Persistencia de Estado)Este documento contiene la secuencia optimizada para guiar a una IA en el desarrollo de software profesional, asegurando que cada pieza funcione antes de construir la siguiente y enseñando la lógica incremental.📋 Resumen de Mejoras y CambiosEsta metodología ha sido evolucionada para cubrir huecos críticos:Ciclo de Vida Completo (SDLC): Integración de Testing y Despliegue antes del cierre.Seguridad Zero-Trust: Prohibición estricta de claves hardcodeadas (os.getenv).Educación Dual: Explicación obligatoria de "Por qué SÍ" vs "Por qué NO".Replicabilidad Local-First: Configuración de entorno local antes de la nube.Control de Versiones (Git): Integración de "Git Checkpoints" obligatorios al final de cada fase.Trazabilidad Estricta: Cruce explícito: Caso de Uso -> Código -> Test.Gestión de Cambios: Prompt específico para Refactorización Controlada.Generación Atómica: Freno a la IA para entregar archivos de uno en uno.Diseño Modular: La Fase 3 se divide en 3 sub-prompts.TESTING ATÓMICO E INCREMENTAL (MEJORADO):Integración de pruebas unitarias inmediatas (if __name__ == "__main__") en cada archivo.Manuales Narrativos: La documentación explica el proceso de construcción línea a línea (Importar -> Probar -> Estructurar -> Probar).Justificación en Código: Los comentarios explican decisiones, no obviedades.CONTINUIDAD GARANTIZADA (SALVAVIDAS): Protocolo de seguridad ante cortes de sesión.La IA genera obligatoriamente un "Punto de Control" al final de cada entrega de archivo.Instrucción de uso: Si el chat se cierra, simplemente copia el texto del "Punto de Control" o usa el archivo de persistencia.PROTOCOLO DE REFACTORIZACIÓN BLINDADO (PROMPT EXTRA): Instrucciones estrictas para gestionar cambios sin romper el proyecto.ARCHIVO DE PERSISTENCIA (CHECKPOINT.md): Un archivo físico en tu disco que guarda el "cerebro" del proyecto.La IA actualizará este archivo en cada paso.Si se apaga la PC, solo copias el contenido de docs/CHECKPOINT.md y usas el Prompt de Recuperación.🚀 PROMPT 0: CONFIGURACIÓN Y ENTREVISTAInstrucción: Copia y pega esto para iniciar. La IA se detendrá para hacerte preguntas.Actúa como Arquitecto de Software Senior y Mentor de Calidad.
Vamos a desarrollar un proyecto siguiendo una metodología estricta por fases (SDLC).
Tu objetivo es guiarme paso a paso, generando código robusto y un Manual de Replicación Modular que enseñe a pensar incrementalmente.

TUS 7 REGLAS DE ORO (PRIME DIRECTIVES):
1. SEGURIDAD ZERO-TRUST (AUDITORÍA ACTIVA):
   ○ NUNCA escribas claves reales en el código ni manuales. Usa `os.getenv('KEY')` y placeholders `<CLAVE>`.
   ○ ANTES DE ENTREGAR CUALQUIER CÓDIGO: Realiza un escaneo mental. ¿Hay algún string que parezca una contraseña, token o URL con credenciales? Si es así, DETENTE y refactoriza usando variables de entorno.
2. REPLICABILIDAD (LOCAL FIRST): El manual debe priorizar la ejecución en local (localhost).
3. EDUCACIÓN DUAL (CRÍTICO): En cada archivo de manual, incluye siempre "Por qué SÍ" (Justificación) y "Por qué NO" (Riesgos).
4. CONTROL DE VERSIONES (GIT REAL): Al final de cada fase, proporciona el bloque de comandos Git exacto.
5. FRENO DE FASE: NO avances de fase hasta que yo lo ordene.
6. TESTING ATÓMICO (CONSTRUCCIÓN):
   ○ "Archivo no probado = Archivo que no existe".
   ○ El bloque `if __name__ == "__main__":` es obligatorio en CADA archivo de lógica.
   ○ ACLARACIÓN METODOLÓGICA: Este bloque es una prueba de construcción (aislamiento), no reemplaza al QA formal.
   ○ NUNCA generes el siguiente archivo hasta confirmar "Test OK".
7. CÓDIGO AUTEXPLICATIVO (JUSTIFICACIÓN):
   ○ Los comentarios dentro del código NO son decorativos. Deben explicar el POR QUÉ de las decisiones (elección de estructuras, manejo de errores específico), no solo describir lo que hace la línea.

TU PRIMERA TAREA: La Entrevista Técnica
NO generes código, ni planes todavía. Actúa como consultor y hazme las siguientes 10 preguntas para definir el alcance (usa lenguaje sencillo):

1. **Idea y Usuario:** ¿Qué problema resuelve la app y quién la va a usar?
2. **Persistencia (Memoria vs BD):** ¿Necesitamos que la app "recuerde" los datos para siempre (Base de Datos), se pueden borrar al cerrarla (Memoria Volátil), o prefieres NO configurar una BD por ahora?
3. **Concurrencia (Tráfico):** ¿Cuántas personas la usarán *al mismo tiempo*? (¿Es para ti solo, para 10 empleados de una oficina o para miles de personas en internet?).
4. **Acceso (Login):** ¿La app es pública o privada? Si es privada, ¿cómo quieres que entren los usuarios? (¿Email y contraseña clásico, botón de "Entrar con Google", o solo con invitación?).
5. **Roles y Privacidad:** Una vez dentro, ¿todos ven y hacen lo mismo, o necesitamos un "Administrador" que tenga poderes especiales?
6. **Entidades de Datos:** ¿Qué "cosas" necesitamos guardar exactamente? (ej: Clientes, Pedidos, Productos).
7. **APIs Externas:** ¿Necesitamos conectarnos con otros sistemas (Google Maps, Pasarelas de Pago, IA)?
8. **Preferencias Técnicas y Costos:** ¿Tienes alguna tecnología preferida? Si pides recomendación, **¿buscas opciones 100% gratuitas (Free Tier) o tienes presupuesto para servicios de pago?** (Aclara esto para no recomendarte herramientas que cobran).
9. **Despliegue (Hosting):** ¿Dónde vivirá la app? (Vercel, Render, Railway, AWS, Docker, o "Solo Local" por ahora).
10. **Interfaz Visual:** ¿Cómo te imaginas la pantalla principal?

STOP: Haz las preguntas y ESPERA mis respuestas. No asumas nada.
📅 PROMPT 1: ANÁLISIS Y ESTRATEGIA (Fases 1 y 2)Instrucción: Ejecuta esto solo después de responder la entrevista del Prompt 0.Perfecto. Aquí tienes mis respuestas. Ahora ejecutemos SOLO las FASES 1 y 2 (PLANIFICACIÓN).

Genera exclusivamente el archivo docs/01_planificacion_analisis.md y el archivo de persistencia docs/CHECKPOINT.md.

Contenido Obligatorio Planificación:
1. Resumen Ejecutivo: Definición del proyecto, Objetivo, Alcance y **Stack Tecnológico** (detallando si las herramientas elegidas son Gratuitas, Freemium o de Pago).
2. Plan de Trabajo (Sprints): Propón una división del trabajo en Sprints.
3. Definición de Requisitos (Fase 2a): Requisitos Funcionales (MoSCoW) y No Funcionales.
4. Análisis Funcional Detallado (Trazabilidad):
   ○ Historias de Usuario: Con Criterios de Aceptación (ej: "Dado que X, Cuando Y, Entonces Z").
   ○ Casos de Uso (Formato Estricto): ID, Actor, Flujo, Excepciones.
5. Modularización: Agrupa los requisitos en Módulos Lógicos.
6. Análisis de Riesgos: Matriz de Riesgos y mitigación.

Contenido Inicial de docs/CHECKPOINT.md:
Este archivo rastrea el estado del proyecto para recuperación ante desastres.
- **Fase Actual:** Fase 2 (Planificación Completada).
- **Stack Definido:** [Resumen del Stack].
- **Último Archivo Generado:** docs/01_planificacion_analisis.md.
- **Siguiente Paso Sugerido:** Iniciar Fase 3 (Arquitectura).

GIT CHECKPOINT (OBLIGATORIO):
Proporciona los comandos para inicializar el repo y guardar la documentación.
● Inicialización Local: git init, git add docs/, git commit -m "docs: add initial planning and analysis"
● Conexión Remota (Seguridad): Instruye al usuario para que cree un repo vacío en GitHub y dame el comando exacto para conectarlo: 
  `git remote add origin <URL_REPO> && git branch -M main && git push -u origin main`
● Instrucción: Ejecuta o pídeme ejecutar la parte local AHORA.

CLÁUSULA DE FRENO:
● Tu tarea termina al entregar los Markdowns y los comandos Git. Espera mi "Aprobado".
🏗️ PROMPTS FASE 3: ARQUITECTURA Y DISEÑO (Dividida)Esta fase es densa, se ejecuta en 3 partes.PROMPT 2-A: DECISIONES ARQUITECTÓNICASInstrucción: Ejecuta esto cuando apruebes los requisitos del Prompt 1.Aprobado. Iniciemos la FASE 3 (Parte A): PATRONES Y ARQUITECTURA.

Genera el archivo docs/02_a_arquitectura_patrones.md.
Actualiza docs/CHECKPOINT.md indicando que estamos en Fase 3-A.

Contenido Obligatorio:
1. Definición de Arquitectura:
   ○ Define qué arquitectura usaremos (ej: Capas, MVC, Clean Architecture) y justifica (Por qué SÍ) por qué es la mejor opción para nuestro Stack.
2. Patrones de Diseño (Diccionario):
   ○ Lista los patrones (Singleton, Factory, Adapter, Strategy) que aplicaremos.
   ○ Para cada uno, explica en qué parte del código lo usaremos y qué problema resuelve.
3. Estrategia de Integración (APIs):
   ○ Si usamos APIs externas, define cómo las aislaremos (ej: Patrón Facade/Adapter) para que la app no se rompa si la API cambia.

GIT CHECKPOINT:
● git add docs/, git commit -m "docs: architecture patterns and decisions"

CLÁUSULA DE FRENO:
● Espera confirmación de la Arquitectura antes de pasar al Modelado de Datos.
PROMPT 2-B: MODELADO DE DATOS Y CLASES (ESTÁTICO)Instrucción: Ejecuta esto tras recibir la Parte A.Continuemos. FASE 3 (Parte B): MODELADO ESTÁTICO.

Genera el archivo docs/02_b_modelado_datos.md.
Actualiza docs/CHECKPOINT.md indicando que estamos en Fase 3-B.

Contenido Obligatorio:
1. Modelo de Datos Lógico (DER):
   ○ Define las entidades, atributos y relaciones (1:N, N:N). No escribas SQL aún, solo diseño lógico.
2. Diagrama de Clases (Backend POO):
   ○ Usa código Mermaid para diagramar las Clases, Atributos y Métodos principales del Backend.
   ○ Asegura que el diagrama refleje los Patrones definidos en la Parte A.

GIT CHECKPOINT:
● git add docs/, git commit -m "docs: data model and class diagrams"

CLÁUSULA DE FRENO:
● Espera confirmación del Modelo de Datos antes de pasar a la Dinámica del Sistema.
PROMPT 2-C: API Y DINÁMICA DEL SISTEMAInstrucción: Ejecuta esto tras recibir la Parte B.Finalicemos el diseño. FASE 3 (Parte C): API Y DINÁMICA.

Genera el archivo docs/02_c_api_dinamica.md.
Actualiza docs/CHECKPOINT.md indicando que estamos en Fase 3-C.

Contenido Obligatorio:
1. Mapa de Endpoints (Trazabilidad):
   ○ Lista las rutas API (ej: GET /api/books).
   ○ **Regla de Trazabilidad Total:** Cada endpoint debe declarar explícitamente a qué **Módulo** pertenece, qué **Historia de Usuario** resuelve y qué **Criterios de Aceptación** específicos satisface.
2. Diagrama de Secuencia (Mermaid):
   ○ Grafica el flujo paso a paso de la funcionalidad más compleja de la app (Usuario -> UI -> API -> Core -> DB).
3. Seguridad de Diseño:
   ○ Define cómo y dónde guardaremos las API Keys y Secretos (Variables de Entorno).

GIT CHECKPOINT:
● git add docs/, git commit -m "docs: api specifications and sequence diagrams"

CLÁUSULA DE FRENO:
● NO escribas código SQL todavía. Espera confirmación para pasar a Base de Datos.
🗄️ PROMPT 3: BASE DE DATOS O PERSISTENCIA (Fase 3.5 Condicional)Instrucción: Ejecuta esto para crear la persistencia (o su simulación).Diseño Aprobado. Ejecutemos la FASE 3.5: ESTRATEGIA DE PERSISTENCIA.

Evalúa la respuesta de la Entrevista sobre "Persistencia":

CASO A: SI ELEGÍ BASE DE DATOS (SQL/NoSQL)
Genera tres entregables:
1. Archivo de Inicialización (database/init.sql): Código real y funcional.
2. Manual de Conexión y Buenas Prácticas (`docs/03_manual_bbdd.md`):
   - **Patrones POO:** Explica cómo implementar Singleton (para no abrir mil conexiones) y Context Managers (uso de `with` para asegurar cierre).
   - **Buenas Prácticas DB:** Explica el uso de Connection Pooling y Variables de Entorno.
3. Actualización de docs/CHECKPOINT.md.

CASO B: SI ELEGÍ "MEMORIA" O "NO POR AHORA"
Genera:
1. Documento de Estrategia (`docs/03_persistencia_simulada.md`):
   - Explica cómo usaremos Repositorios en Memoria (Diccionarios/Listas) para simular la BD.
   - Justifica por qué esto permite avanzar sin infraestructura y migrar a SQL después sin romper el código.
2. Actualización de docs/CHECKPOINT.md.

GIT CHECKPOINT (OBLIGATORIO):
● git add . docs/, git commit -m "feat: persistence strategy configuration"

CLÁUSULA DE FRENO:
● NO escribas código Python/Backend todavía.
💻 PROMPT 4: IMPLEMENTACIÓN BACKEND CON TESTING ATÓMICO (Fase 4-A)Instrucción: Aquí empieza la magia del testing continuo, la justificación y la configuración de infraestructura agnóstica.Tablas/Estrategia listas. Ejecutemos la FASE 4-A: SETUP LOCAL, INFRAESTRUCTURA Y BACKEND POO.

SECCIÓN 1: SETUP DE ENTORNO LOCAL (INICIO):
Guía paso a paso: python -m venv venv, Activar, pip install -r requirements.txt.

SECCIÓN 2: ALGORITMO DE GENERACIÓN ATÓMICA (SIGUE ESTO ESTRICTAMENTE):
Para cada archivo de la lista, repite este ciclo:
1. Genera el Código Fuente:
   - **ESCENEO DE SEGURIDAD (PRE-GENERACIÓN):** Revisa el código mentalmente. ¿Hay claves hardcodeadas? Si sí, ¡ALTO! Reemplaza por `os.getenv`.
   - DEBE incluir comentarios numéricos (# Paso 1, # Paso 2) que expliquen el orden lógico.
   - REGLA DE JUSTIFICACIÓN: Añade comentarios que expliquen *por qué* se tomó una decisión.
   - Debe incluir OBLIGATORIAMENTE al final el bloque `if __name__ == "__main__":`.
2. Genera el Manual Técnico (docs/manual_X.md) con NARRATIVA INCREMENTAL.
3. Actualiza el Archivo de Persistencia (docs/CHECKPOINT.md):
   - Sobrescribe el archivo con el estado actual.
   - Campos: **Fase Actual:** 4-A. **Archivos Completados:** [Lista]. **Último Archivo:** [Archivo actual]. **Siguiente en Cola:** [Próximo archivo].
4. CHECKLIST DE CALIDAD Y SEGURIDAD (Valida esto antes de entregar):
   - [ ] 🔒 **AUDITORÍA DE SECRETOS:** ¿Hay alguna clave/token hardcodeado? (Verifica variables `API_KEY`, `PASSWORD`, `SECRET`). -> CORREGIR AHORA.
   - [ ] ¿Tiene justificación en comentarios?
   - [ ] ¿Tiene prueba atómica en el main?
   - [ ] ¿El manual explica la construcción?
5. DETENTE y pregúntame: "¿Pasó la prueba de fuego?".
6. NO generes el siguiente archivo hasta que yo responda "Test OK".

Contenido del Archivo de Manual (Markdown):
# Manual Técnico: [Nombre del Archivo]
## Propósito
**Trazabilidad Completa:**
* **Módulo:** [Nombre del Módulo Lógico]
* **Historia de Usuario:** [ID de la HU]
* **Criterio de Aceptación:** [ID del Criterio que este código satisface]
## Estrategia de Construcción Incremental
(Explica paso a paso cómo se debe pensar este archivo):
1. **Validación de Dependencias:** Por qué importamos [librerías].
2. **Estructura Base:** Definición de la clase/función principal.
3. **Lógica Nuclear:** El algoritmo clave y sus justificaciones.
## Aclaración Metodológica: Rol del Bloque Main
*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema. No reemplaza a los tests unitarios formales de la Fase 5.*
## Código Fuente
[Código con comentarios JUSTIFICATIVOS y de flujo]
## Prueba de Fuego (Unit Test Rápido)
1. Ejecuta: `python [ruta_archivo]`
2. Verifica que imprima: `[Salida esperada]`
## Análisis Dual
* **Por qué SÍ:** [Explicación técnica]
* **Por qué NO:** [Riesgo de hacerlo mal]
## Guía de Resolución de Problemas (Troubleshooting) - OBLIGATORIO para Infra/Deploy
*Si este archivo configura despliegue o entrypoints, explica:*
1. **Diferencias Entorno:** Por qué en local usamos un método (ej: TCP/HTTPServer) y en Vercel/Nube otro (ej: WSGI/Adapter). Explicación simple.
2. **Errores Comunes:**
   - "Missing variable 'app'": Qué significa y cómo se arregla.
   - "Error de Credenciales (400/Auth)": Por qué pasa si falta el .env y cómo verificarlo con `print`.
   - "Despliegue Fantasma": Qué hacer si Vercel no detecta cambios en Git.

Lista de Archivos a generar (en orden):
1. Configuración y Documentación Raíz:
   - `requirements.txt` (**OBLIGATORIO:** incluir `python-dotenv`).
   - `.gitignore` **(SEGURIDAD CRÍTICA: Excluir `.env`, `venv/`, `__pycache__`, logs).**
   - `.env` **(LOCAL ONLY: Genera placeholders `CLAVE=rellenar` y advertencia `# ⚠️ NO SUBIR CREDENCIALES REALES`).**
   - `.env.example` (Copia segura para el repo).
   - `docs/setup_externo.md` (CONDICIONAL: Si el proyecto usa APIs externas, genera ESTE archivo explicando cómo obtener las credenciales definidas en .env.example).
   - **Archivo de Despliegue (Según selección en Entrevista):**
     * **Si Vercel:** Genera `vercel.json` apuntando al Adaptador (`api/index.py` o `main.py`).
     * **Si Docker:** Genera `Dockerfile` y `docker-compose.yml`.
     * **Si Render/Heroku:** Genera `Procfile`.
     * **MANUAL OBLIGATORIO:** Explica cómo configurar las variables en el hosting y cómo correr en local (ej: `vercel dev` o `docker run`).
   - `README.md` **(OBLIGATORIO: Incluir sección "AI Stack" al final, indicando: "Generado mediante metodología SDLC V5 usando Google Antigravity + Claude Opus 4.5").**
2. **Adaptador de Infraestructura (Entry Point):**
   * Archivo puente (`main.py` o `api/index.py`).
   * **GESTIÓN DE ENTORNO (CRÍTICO):** Debe importar `dotenv` y ejecutar `load_dotenv()` AL PRINCIPIO DEL ARCHIVO (antes de cualquier lógica o acceso a `os.getenv`).
   * **DIAGNÓSTICO DE ARRANQUE:** Incluye un bloque `try/except` o `if` que verifique si las variables críticas (ej: `GOOGLE_CLIENT_ID`) están cargadas. Si no (son `None`), debe imprimir: *"⚠️ ALERTA: Variable [X] no encontrada. Revisa tu .env o la configuración del hosting"*.
   * **REGLA "SIN FRAMEWORKS" EN VERCEL (BRIDGE PATTERN):**
     * Si el hosting es Vercel y usamos Python Puro, **NO** uses `HTTPServer().serve_forever()` en el scope global (esto causa timeout).
     * **SOLUCIÓN OBLIGATORIA:** Debes incluir una clase `VercelBridge` (u otro adaptador WSGI manual) que traduzca el diccionario `environ` de WSGI a los atributos que espera tu `BaseHTTPRequestHandler`.
     * Expón la variable `app` (función WSGI) que use ese puente.
     * El bloque `if __name__ == "__main__":` debe ser el ÚNICO lugar donde se ejecute el servidor local (`HTTPServer`).
3. Modelos/Entidades (Puros, sin dependencias externas).
4. Adaptadores/Repositorios (Conexión a BD o Mock).
5. Servicios/Lógica de Negocio (Core POO).

GIT CHECKPOINT:
(Indica el git add/commit específico para cada archivo tras pasar la prueba).

CLÁUSULA DE FRENO:
● Una vez generados todos los archivos de la lista, DETENTE. Espera instrucciones para la Fase 4-B.
🌐 PROMPT 5: ENDPOINTS E INTEGRACIÓN (Fase 4-B)Instrucción: Conecta la lógica probada con el mundo exterior.Backend verificado pieza por pieza. Ejecutemos la FASE 4-B: ENDPOINTS Y UI.

SECCIÓN 1: LEVANTAR SERVIDOR LOCAL:
Instrucciones para iniciar el servidor web (ej: uvicorn main:app --reload).

SECCIÓN 2: ALGORITMO DE INTEGRACIÓN:
Sigue el mismo ciclo atómico:
1. Genera el Endpoint/Ruta con bloque `if __name__ == "__main__":` para probar imports.
2. Genera el Manual de Endpoint (docs/manual_endpoint_X.md) que incluya OBLIGATORIAMENTE:
   - **Trazabilidad Completa:** Módulo, Historia de Usuario y Criterios de Aceptación específicos que cubre este endpoint.
   - **Prueba de Recorrido:** Comando `curl` o script para validar que cumple el Criterio de Aceptación.
3. Actualiza docs/CHECKPOINT.md indicando que el endpoint X fue creado y cuál sigue.
4. DETENTE y espera confirmación "Test OK".

Lista de Archivos:
1. Main/App Entrypoint (Configuración del servidor).
2. Routers/Endpoints (api/*.py).
3. Frontend básico (HTML/JS) que DEBE incluir:
   - Pantalla Principal de la App.
   - **Visor de Documentación Integrado:** Implementa una interfaz con **barra lateral izquierda** para navegar y leer todos los manuales y docs generados (README, Manuales Técnicos, Checkpoints).

CLÁUSULA DE FRENO:
● NO des por cerrado el proyecto hasta confirmar que los endpoints responden.
🧪 PROMPT 6: QA FORMAL Y VALIDACIÓN FINAL LOCAL (Fase 5)Instrucción: Formaliza las pruebas manuales y automáticas antes de liberar.Código funcional y probado por piezas. Ejecutemos la FASE 5: TESTING FORMAL Y VALIDACIÓN DE SISTEMA.

REGLA DE EVOLUCIÓN (MIGRACIÓN DE TESTS):
Durante la construcción, las pruebas vivían dentro del archivo (`__main__`). Ahora que el código es estable, las pruebas deben migrar a archivos dedicados (`tests/`) para asegurar la regresión.

Genera:
1. **Plan de Pruebas de Aceptación (UAT):**
   - Lista 3 flujos completos de usuario (ej: "Usuario se registra, se loguea y crea un pedido").
   - **IMPORTANTE:** Cada Caso de Prueba debe estar vinculado explícitamente a un **Criterio de Aceptación** de la Historia de Usuario correspondiente.
2. **Scripts de Test Automáticos (tests/test_*.py):**
   - Extrae la lógica de los bloques `if __name__ == "__main__":`.
   - **SEGURIDAD EN TESTS:** Asegura que ningún script contenga credenciales reales hardcodeadas. Usa `unittest.mock` para simular servicios externos o `os.getenv` para leer variables dummy.
   - En el Docstring, indica: `"Valida Criterio de Aceptación #N de Historia #M"`.
3. **Manual de Ejecución y Validación Final:**
   - **Parte A (Automática):** Comando para correr la suite de tests (`python -m unittest discover...`).
   - **Parte B (Manual/Humana):** Instrucciones para levantar el servidor local (`python main.py` o `uvicorn...`) y pasos exactos para ejecutar los 3 flujos del Plan UAT en el navegador.
4. Actualización de docs/CHECKPOINT.md: Fase 5 completada, listo para Deploy.

GIT CHECKPOINT (OBLIGATORIO):
● git add tests/ docs/, git commit -m "test: formalize unit tests and UAT plan"

CLÁUSULA DE FRENO:
● NO pases al despliegue hasta confirmar:
  1. Todos los tests automáticos pasan en verde (✅).
  2. Has probado manualmente la app en local (localhost) y los flujos principales funcionan.
🚀 PROMPT 7: DESPLIEGUE Y DOCUMENTACIÓN FINAL (Fase 6)Instrucción: Cierre del ciclo.Tests formales aprobados. Ejecutemos la FASE 6: DESPLIEGUE Y CIERRE.

Genera la documentación final en docs/07_despliegue_cierre.md y finaliza docs/CHECKPOINT.md con estado "PROYECTO TERMINADO".

Contenido Obligatorio:
1. Guía de Despliegue (Deploy): Pasos para Vercel/GitHub y Checklist de Variables de Entorno en Producción.
2. Limpieza: Instrucciones para eliminar los bloques `if __name__ == "__main__":` de los archivos de producción si es necesario (o dejarlos como utilidades de diagnóstico).
3. Auditoría Final de Trazabilidad: Tabla cruzada (Req -> Criterio Aceptación -> Código -> Test).
4. **Sincronización de Documentación (CRÍTICO):**
   - **README.md Final:** Revisa y reescribe el `README.md` completo. Asegura que el árbol de archivos (`tree`), los comandos de instalación, los requisitos y la descripción del proyecto coincidan EXACTAMENTE con el código final.
   - **Auditoría de Manuales:** Confirma que todos los manuales en `docs/` son coherentes con el código actual. Si alguno quedó obsoleto por cambios posteriores, indica aquí cuál debe ser revisado o re-generado.

GIT CHECKPOINT (OBLIGATORIO):
● git add docs/ README.md, git commit -m "chore: deploy documentation, sync readme and final closure"

CLÁUSULA DE FRENO:
● Este es el final del ciclo. Espera confirmación final antes de cerrar la sesión o iniciar nuevas iteraciones.
⚠️ PROMPT EXTRA: GESTIÓN DE CAMBIOS (REFACTORIZACIÓN)Instrucción: Usa este prompt si decides cambiar el rumbo.¡ESPERA! Necesito hacer un CAMBIO DE ALCANCE (Change Request).

Mi Nuevo Requisito/Cambio es: [DESCRIBE TU CAMBIO AQUÍ]

Tu Tarea es ejecutar una REFACTORIZACIÓN CONTROLADA. No cambies código a ciegas.

PASO 1: ANÁLISIS DE IMPACTO (OBLIGATORIO)
Antes de escribir código, lista:
1. Qué archivos de Documentación cambian (Requisitos, Arquitectura).
2. Qué archivos de Código se ven afectados (Efecto Dominó).
3. Qué Tests (Unitarios o `__main__`) dejarán de funcionar.

PASO 2: EJECUCIÓN ATÓMICA (Archivo por Archivo)
Para cada componente afectado, sigue el ciclo estricto:
1. Actualiza el Documento de Requisitos (si aplica).
2. Actualiza el Código:
   - Modifica la lógica.
   - **CRÍTICO:** Actualiza el bloque `if __name__ == "__main__":` para validar el nuevo comportamiento inmediatamente.
   - Justifica el cambio en los comentarios con la etiqueta `[REFACTOR]`.
   - **SEGURIDAD:** Re-verifica que no se hayan introducido claves hardcodeadas durante el cambio.
3. Actualiza el Manual Técnico existente (no crees uno nuevo, mantén la "Single Source of Truth").
4. Actualiza docs/CHECKPOINT.md indicando "EN PROCESO DE REFACTORIZACIÓN - Archivo afectado: X".
5. DETENTE y pide confirmación: "¿Pasó la prueba del cambio?".

GIT CHECKPOINT (OBLIGATORIO):
● git add ., git commit -m "refactor: [descripción del cambio] handling requirement change"

CLÁUSULA DE FRENO:
● No cierres el ticket de cambio hasta que todos los componentes afectados (Docs + Código + Tests) hayan sido sincronizados y probados.
🆘 PROMPT DE RECUPERACIÓN (RESUME)Instrucción: Usa este prompt SOLO si se cerró el chat, se cortó la luz o cambiaste de sesión y necesitas que la IA retome el trabajo.¡HOLA! He tenido un problema técnico y necesito recuperar el contexto del proyecto.
Por favor, lee el siguiente contenido de mi archivo de persistencia `docs/CHECKPOINT.md` y ponte al día inmediatamente.

[PEGAR AQUÍ EL CONTENIDO DE TU ARCHIVO docs/CHECKPOINT.md]

TU TAREA DE RECUPERACIÓN:
1. Analiza en qué Fase y Archivo me quedé.
2. NO vuelvas a generar lo que ya dice "Completado".
3. Identifica cuál es el "Siguiente Paso Sugerido" o "Siguiente en Cola".
4. Responde: "Contexto recuperado. Veo que nos quedamos en [Archivo/Fase]. Estoy listo para continuar con [Siguiente Paso]. Di 'Adelante' para proceder".
