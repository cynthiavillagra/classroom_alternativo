**SECUENCIA MAESTRA DE PROMPTS PROGRESIVOS**

(Con Freno de Fase, Git Flow, Seguridad Zero-Trust, Testing Atómico, Persistencia y Arquitectura Universal)

Este documento contiene la secuencia optimizada para guiar a una IA en el desarrollo de software profesional, asegurando que cada pieza funcione antes de construir la siguiente y enseñando la lógica incremental.

**📋 Resumen de Mejoras y Cambios**

Esta metodología ha sido evolucionada para cubrir huecos críticos y mejoras estructurales:

1. Ciclo de Vida Completo (SDLC): Integración de Testing y Despliegue antes del cierre.

2. Seguridad Zero-Trust: Prohibición estricta de claves hardcodeadas (os.getenv).

3. Educación Dual: Explicación obligatoria de "Por qué SÍ" vs "Por qué NO".

4. Replicabilidad Local-First: Configuración de entorno local antes de la nube.

5. Control de Versiones (Git): Integración de "Git Checkpoints" obligatorios al final de cada fase.

6. Trazabilidad Estricta: Cruce explícito: Caso de Uso \-\> Código \-\> Test.

7. Gestión de Cambios: Prompt específico para Refactorización Controlada.

8. Generación Atómica: Freno a la IA para entregar archivos de uno en uno.

9. Diseño Modular: La Fase 3 se divide en 3 sub-prompts.

10. Testing atómico e incremental: Pruebas unitarias inmediatas (if **name** \== "**main**") en cada archivo.

11. Continuidad garantizada: Protocolo de seguridad ante cortes de sesión (Puntos de Control).

12. Protocolo de refactorización blindado: Instrucciones estrictas para gestionar cambios.

13. Archivo de persistencia (CHECKPOINT.md): Rastreo de estado en disco.

14. Arquitectura stateless: Regla obligatoria para Vercel/Serverless (evitar memoria volátil para sesiones).

15. Cero placeholders: Regla de UI, si se ve, funciona.

16. Estructura homogénea interna: Unificación de secciones repetidas (Contenido Obligatorio, Git Checkpoint, Cláusula de Freno) en todos los prompts.

**Resumen de Requerimientos de Seguridad Adicionales (aporte de Gonzalo)**

He analizado tu petición y los puntos clave a integrar en la secuencia de prompts son:

1. Hardcode Zero Tolerance: Prohibición absoluta de credenciales en el código. Uso obligatorio de variables de entorno.

2. No Session Caching: Evitar el almacenamiento inseguro de sesiones en caché local o volátil que pueda ser explotado.

3. Active Session Validation (Middleware/Backend): Por cada transacción o llamada a API, el sistema debe validar obligatoriamente si la sesión del usuario sigue activa y es válida.

4. Forced Inactivity Timeout (15 min): Implementar un "Watchdog" (perro guardián) que registre la última interacción. Si pasan más de 15 minutos, la sesión se invalida en el backend.

5. UX Expiration Notice (Frontend): Implementar un aviso visual (modal, notificación o redirección con mensaje) que informe al usuario: "Su sesión ha expirado por inactividad. Por favor, inicie sesión nuevamente".

**🚀 PROMPT 0: CONFIGURACIÓN Y ENTREVISTA**

*(Estilo Word: Título 2\)*  
Instrucción: Copia y pega esto para iniciar. La IA se detendrá para hacerte preguntas.  
Actúa como Arquitecto de Software Senior y Mentor de Calidad.  
Vamos a desarrollar un proyecto siguiendo una metodología estricta por fases (SDLC).  
Tu objetivo es guiarme paso a paso, generando código robusto y un Manual de Replicación Modular.

**TUS 10 REGLAS DE ORO (PRIME DIRECTIVES):**

---

**SEGURIDAD Y ARQUITECTURA**

1. Seguridad Zero-Trust  
   Nunca escribas claves reales. Usá siempre os.getenv('KEY').  
   Está terminantemente prohibido el hardcodeo de credenciales.

2. Arquitectura Stateless (Universal)  
   o Si el despliegue es serverless (Vercel, AWS Lambda), nunca guardes estado en la memoria RAM del servidor (por ejemplo: session \= {} o variables globales modificables).  
   o El estado debe manejarse mediante cookies firmadas, JWT o base de datos.  
   o PROHIBIDO: El cacheo de sesiones en capas inseguras o variables globales volátiles.  
   o WATCHDOG DE INACTIVIDAD: Implementa un cierre de sesión forzado tras 15 minutos de inactividad detectada en los servicios/API.  
   o VALIDACIÓN TRANSACCIONAL: Cada llamada a un servicio o API debe validar obligatoriamente si la sesión del usuario sigue activa.

3. Fechas seguras  
   Para comparaciones de tiempo, utilizá siempre datetime.now(timezone.utc).

---

**PROCESO Y CALIDAD**

4. Replicabilidad (Local First)  
   Priorizá que la aplicación funcione correctamente en localhost antes de desplegarla en la nube.

5. Educación dual  
   Explicá siempre el “por qué SÍ” y el “por qué NO” de cada decisión técnica.

6. Control de versiones  
   Proporcioná los comandos de Git correspondientes al final de cada fase.

7. Freno de fase  
   No avances a la siguiente etapa hasta que yo lo indique explícitamente.

8. Testing atómico  
   “Archivo no probado \= archivo que no existe”.  
   Todo archivo debe incluir su bloque:

9. if **name** \== "**main**":

10. Cero placeholders  
    En el frontend, todo botón o enlace debe funcionar o estar oculto.  
    No entregues Lorem Ipsum ni elementos sin lógica funcional.

11. Código autoexplicativo  
    Usá comentarios justificativos (POR QUÉ), no descriptivos (QUÉ).

---

**TU PRIMERA TAREA: LA ENTREVISTA TÉCNICA**

No generes código todavía.  
Realizá las siguientes 10 preguntas para definir el alcance del proyecto:

1. Idea y usuario  
   ¿Qué problema resuelve la app y quién la va a usar?

2. Persistencia (Memoria vs Base de Datos)  
   ¿La aplicación debe recordar datos de forma permanente (BD), borrarlos al cerrar (memoria) o preferís no configurar una base de datos por ahora?

3. Concurrencia  
   ¿Será de uso personal o para múltiples usuarios simultáneos?

4. Acceso (Login)  
   ¿Aplicación pública o privada? ¿Google, email o invitación?

5. Roles  
   ¿Todos los usuarios tienen los mismos permisos o existen administradores?

6. Entidades de datos  
   ¿Qué información se va a almacenar? (por ejemplo: clientes, pedidos).

7. APIs externas  
   ¿Debe integrarse con otros sistemas o servicios externos?

8. Preferencias técnicas  
   ¿Tecnologías preferidas? ¿Presupuesto free o pago?

9. Despliegue (Hosting)  
   ¿Dónde va a vivir la aplicación? (Vercel, Docker, local).  
   Nota: esta decisión define si se utiliza arquitectura stateless.

10. Interfaz visual  
    ¿Cómo imaginás la pantalla principal?

---

STOP: Haz las preguntas y ESPERA mis respuestas.

**📅 PROMPT 1: ANÁLISIS Y ESTRATEGIA (Fases 1 y 2\)**

*(Estilo Word: Título 2\)*  
Instrucción: Ejecuta esto solo después de responder la entrevista del Prompt 0\.  
Perfecto. Aquí tienes mis respuestas. Ahora ejecutemos SOLO las FASES 1 y 2 (PLANIFICACIÓN).

Genera exclusivamente el archivo docs/01\_planificacion\_analisis.md y el archivo de persistencia docs/CHECKPOINT.md.

**Contenido Obligatorio – Planificación**

1. Resumen Ejecutivo: Definición del proyecto, Objetivo, Alcance y Stack Tecnológico.

2. Plan de Trabajo (Sprints): Propón una división del trabajo en Sprints.

3. Definición de Requisitos (Fase 2a): Requisitos Funcionales (MoSCoW) y No Funcionales.

4. Análisis Funcional Detallado (Trazabilidad):  
   ○ Historias de Usuario: Con Criterios de Aceptación.  
   ○ Casos de Uso (Formato Estricto).

5. Modularización: Agrupa los requisitos en Módulos Lógicos.

6. Análisis de Riesgos: Matriz de Riesgos y mitigación (Incluir riesgo de "Memoria Volátil" si se eligió Serverless).

**Contenido Inicial de docs/CHECKPOINT.md**

* **Fase Actual:** Fase 2 (Planificación Completada).

* **Stack Definido:** \[Resumen del Stack\].

* **Último Archivo Generado:** docs/01\_planificacion\_analisis.md.

* **Siguiente Paso Sugerido:** Iniciar Fase 3 (Arquitectura).

**GIT CHECKPOINT (OBLIGATORIO):**

Proporciona los comandos para inicializar el repo y guardar la documentación.  
● Inicialización Local: git init, git add docs/, git commit \-m "docs: add initial planning"  
● Conexión Remota (Seguridad): Comandos para conectar a GitHub.  
● Instrucción: Ejecuta o pídeme ejecutar la parte local AHORA.

**CLÁUSULA DE FRENO:**

● Tu tarea termina al entregar los Markdowns y los comandos Git. Espera mi "Aprobado".

**🏗️ PROMPTS FASE 3: ARQUITECTURA Y DISEÑO (Dividida)**

*(Estilo Word: Título 2\)*  
Esta fase es densa, se ejecuta en 3 partes.

**PROMPT 2-A: DECISIONES ARQUITECTÓNICAS**

*(Estilo Word: Título 3\)*  
Instrucción: Ejecuta esto cuando apruebes los requisitos del Prompt 1\.  
Aprobado. Iniciemos la FASE 3 (Parte A): PATRONES Y ARQUITECTURA.

Genera el archivo docs/02\_a\_arquitectura\_patrones.md.  
Actualiza docs/CHECKPOINT.md indicando que estamos en Fase 3-A.

**Contenido Obligatorio**

1. Definición de Arquitectura:  
   ○ Define la arquitectura y justifica (Por qué SÍ).

2. Patrones de Diseño (Diccionario):  
   ○ Lista los patrones (Singleton, Factory, Adapter, Strategy) que aplicaremos.

3. Estrategia de Integración (APIs):  
   ○ Si usamos APIs externas, define cómo las aislaremos.

4. **Estrategia Stateless (Si aplica):**  
   ○ Si el despliegue es Vercel/Serverless, define explícitamente cómo manejaremos el estado (Cookies, BD Externa) y prohíbe el uso de variables globales para almacenamiento.

GIT CHECKPOINT:  
● git add docs/, git commit \-m "docs: architecture patterns and decisions"

CLÁUSULA DE FRENO:  
● Espera confirmación de la Arquitectura.

**PROMPT 2-B: MODELADO DE DATOS Y CLASES (ESTÁTICO)**

*(Estilo Word: Título 3\)*  
Instrucción: Ejecuta esto tras recibir la Parte A.  
Continuemos. FASE 3 (Parte B): MODELADO ESTÁTICO.

Genera el archivo docs/02\_b\_modelado\_datos.md.  
Actualiza docs/CHECKPOINT.md indicando que estamos en Fase 3-B.

Contenido Obligatorio:

1. Modelo de Datos Lógico (DER).

2. Diagrama de Clases (Backend POO):  
   ○ Usa código Mermaid.  
   ○ Asegura que el diagrama refleje los Patrones definidos en la Parte A.

GIT CHECKPOINT:  
● git add docs/, git commit \-m "docs: data model and class diagrams"

CLÁUSULA DE FRENO:  
● Espera confirmación del Modelo de Datos.

**PROMPT 2-C: API Y DINÁMICA DEL SISTEMA**

*(Estilo Word: Título 3\)*  
Instrucción: Ejecuta esto tras recibir la Parte B.  
Finalicemos el diseño. FASE 3 (Parte C): API Y DINÁMICA.

Genera el archivo docs/02\_c\_api\_dinamica.md.  
Actualiza docs/CHECKPOINT.md indicando que estamos en Fase 3-C.

Contenido Obligatorio:

1. Mapa de Endpoints (Trazabilidad):  
   ○ Lista las rutas API.  
   ○ **Regla de Trazabilidad Total:** Cada endpoint debe declarar: Módulo, Historia de Usuario y Criterios de Aceptación.

2. Diagrama de Secuencia (Mermaid).

3. Seguridad de Diseño y Sesión:  
   • Define gestión de API Keys.  
   • Lógica de Watchdog: Describe cómo el backend rastreará el tiempo de la última interacción y el flujo de invalidación automática a los 15 minutos.  
   • Protocolo de Intercepción (Frontend): Define cómo el Front detectará el estado de sesión expirada (ej. catching 401 Unauthorized) para mostrar el aviso al usuario.

GIT CHECKPOINT:  
● git add docs/, git commit \-m "docs: api specifications and sequence diagrams"

CLÁUSULA DE FRENO:  
● NO escribas código SQL todavía. Espera confirmación.

**🗄️ PROMPT 3: BASE DE DATOS O PERSISTENCIA (Fase 3.5 Condicional)**

Instrucción: Ejecuta esto para crear la persistencia.  
Diseño Aprobado. Ejecutemos la FASE 3.5: ESTRATEGIA DE PERSISTENCIA.

Evalúa la respuesta de la Entrevista sobre "Persistencia":

**CASO A: SI ELEGÍ BASE DE DATOS (SQL/NoSQL)**

Genera: database/init.sql y docs/03\_manual\_bbdd.md.

**CASO B: SI ELEGÍ "MEMORIA" O "NO POR AHORA"**

Genera:

1. Documento de Estrategia (docs/03\_persistencia\_simulada.md):

* **ADVERTENCIA CRÍTICA:** Si estás en Vercel/Serverless, explica claramente que la "memoria" se borra cada pocos segundos.

* Define si usaremos un archivo JSON temporal (que también es efímero en Vercel pero sirve para demos) o solo mocks en RAM.

2. Actualización de docs/CHECKPOINT.md.

GIT CHECKPOINT (OBLIGATORIO):  
● git add . docs/, git commit \-m "feat: persistence strategy configuration"

CLÁUSULA DE FRENO:  
● NO escribas código Python/Backend todavía.

**💻 PROMPT 4: IMPLEMENTACIÓN BACKEND CON TESTING ATÓMICO (Fase 4-A)**

Instrucción: Aquí empieza la magia del testing continuo y la configuración robusta.  
Tablas/Estrategia listas. Ejecutemos la FASE 4-A: SETUP LOCAL, INFRAESTRUCTURA Y BACKEND POO.

**SECCIÓN 1: SETUP DE ENTORNO LOCAL (INICIO)**

Guía paso a paso: python \-m venv venv, Activar, pip install \-r requirements.txt.

**SECCIÓN 2: ALGORITMO DE GENERACIÓN ATÓMICA (SIGUE ESTO ESTRICTAMENTE)**

Para cada archivo de la lista, repite este ciclo:

1. Genera el Código Fuente:

* **ESCANEO DE SEGURIDAD:** Revisa claves hardcodeadas.  
  \-**MIDDLEWARE DE SESIÓN:** Implementa el validador por transacción y el contador de 15 minutos de inactividad. Si el tiempo expira, la respuesta debe ser un error de autenticación explícito (401).

* **ESCANEO STATELESS:** Si es Vercel, verifica que no estemos guardando sesiones en variables globales (session\_store \= {}).

* REGLA DE JUSTIFICACIÓN: Comentarios "Por qué".

* Bloque if \_\_name\_\_ \== "\_\_main\_\_": obligatorio.

2. Genera el Manual Técnico (docs/manual\_X.md) con NARRATIVA INCREMENTAL.

3. Actualiza el Archivo de Persistencia (docs/CHECKPOINT.md).

4. CHECKLIST DE CALIDAD:

* 🔒 Auditoría de Secretos.

* ☁️ Compatibilidad Serverless (si aplica).

* Prueba atómica presente.

5. DETENTE y pregúntame: "¿Pasó la prueba de fuego?".

6. NO generes el siguiente archivo hasta recibir "Test OK".

Contenido del Archivo de Manual (Markdown):

**Manual Técnico: \[Nombre del Archivo\]**

**1\. Propósito**

**Trazabilidad Completa:** (Módulo, HU, Criterio).

**2\. Estrategia de Construcción**

**3\. Aclaración Metodológica**

**3.1 Rol del Bloque Main**

**4\. Código Fuente**

**5\. Prueba de Fuego**

**5.1 Unit Test Rápido**

**6\. Análisis Dual**

**7\. Guía de Resolución de Problemas**

**7.1 Troubleshooting**

*Si es Infra/Deploy, explicar diferencias Local vs Nube.*

**Lista de Archivos a generar (en orden)**

1. Configuración y Documentación Raíz:

* requirements.txt (incluir python-dotenv).

* .gitignore (Excluir .env, venv, logs).

* .env (LOCAL con placeholders).

* .env.example (Copia segura).

* docs/setup\_externo.md (CONDICIONAL: Guía paso a paso para APIs externas).

* **Archivo de Despliegue:** vercel.json / Dockerfile / Procfile. Incluir manual de uso Local vs Nube.

* README.md (Con sección "AI Stack").

2. **Adaptador de Infraestructura (Entry Point):**

* main.py o api/index.py.

* load\_dotenv() AL PRINCIPIO.

* **REGLA "SIN FRAMEWORKS" EN VERCEL (BRIDGE PATTERN):**

  * Implementa clase VercelBridge (adaptador WSGI manual).

  * Expón variable app (WSGI).

  * if \_\_name\_\_ \== "\_\_main\_\_": ejecuta HTTPServer.

3. Modelos/Entidades.

4. Adaptadores/Repositorios.

5. Servicios/Lógica de Negocio.

GIT CHECKPOINT:  
(Indica el git add/commit específico).

CLÁUSULA DE FRENO:  
● Una vez generados todos los archivos, DETENTE.

**🌐 PROMPT 5: ENDPOINTS E INTEGRACIÓN (Fase 4-B)**

Instrucción: Conecta la lógica con el mundo exterior.  
Backend verificado. Ejecutemos la FASE 4-B: ENDPOINTS Y UI.

**SECCIÓN 1: LEVANTAR SERVIDOR LOCAL**

Instrucciones para iniciar el servidor web.

**SECCIÓN 2: ALGORITMO DE INTEGRACIÓN**

Sigue el ciclo atómico.

1. Genera el Endpoint/Ruta.

2. Genera el Manual de Endpoint (docs/manual\_endpoint\_X.md) con Trazabilidad y Prueba curl.

3. Actualiza docs/CHECKPOINT.md.

4. DETENTE y espera confirmación.

**Lista de Archivos**

1. Main/App Entrypoint (si requiere updates de rutas).

2. Routers/Endpoints (api/\*.py).

3. Frontend básico (HTML/JS) que DEBE incluir:

* **REGLA CERO PLACEHOLDERS:** Todo botón visible debe funcionar o estar oculto.

* **Visor de Documentación Integrado:** Barra lateral izquierda para leer los docs generados.

* **AVISO DE EXPIRACIÓN (UX):** Debe incluir un sistema de notificación (Modal o Alert estético) que se active cuando el backend informe que la sesión ha expirado.

Mensaje: "Su sesión ha expirado por inactividad. Por favor, inicie sesión nuevamente".

* **REDIRECCIÓN AUTOMÁTICA**: Tras el aviso, el usuario debe ser enviado al login automáticamente.  
  CLÁUSULA DE FRENO:  
  ● NO des por cerrado el proyecto hasta confirmar que los endpoints responden.  
  🛡️ REFUERZO OPERATIVO DE SEGURIDAD (POST-INTEGRACIÓN)  
  ⚠️ INSTRUCCIÓN DE APOYO GLOBAL: "En cada generación de servicio, asegura que el decorador de validación de sesión esté presente y que el contador de inactividad se actualice en cada interacción exitosa. No entregues ningún endpoint que no pase por este filtro de seguridad."

**🧪 PROMPT 6: QA FORMAL Y VALIDACIÓN FINAL LOCAL (Fase 5\)**

Instrucción: Formaliza las pruebas manuales y automáticas.  
Código funcional. Ejecutemos la FASE 5: TESTING FORMAL.

Genera:

1. **Plan de Pruebas de Aceptación (UAT):** 3 flujos completos vinculados a Criterios de Aceptación.

2. **Scripts de Test Automáticos (tests/test\_\*.py):**

* Extrae lógica de \_\_main\_\_.

* **SEGURIDAD:** Sin credenciales reales (usar Mocks).

* **FECHAS:** Usar datetime.now(timezone.utc).

3. **Manual de Ejecución y Validación Final:**

* Parte A: Tests Automáticos.

* Parte B: Validación Manual Humana (UAT en Local).

4. Actualización de docs/CHECKPOINT.md.

GIT CHECKPOINT (OBLIGATORIO):  
● git add tests/ docs/, git commit \-m "test: formalize unit tests and UAT plan"

CLÁUSULA DE FRENO:  
● NO pasar al despliegue hasta confirmar Tests Verdes y UAT Manual OK.

**🚀 PROMPT 7: DESPLIEGUE Y DOCUMENTACIÓN FINAL (Fase 6\)**

Instrucción: Cierre del ciclo.  
Tests aprobados. Ejecutemos la FASE 6: DESPLIEGUE Y CIERRE.

Genera docs/07\_despliegue\_cierre.md y finaliza docs/CHECKPOINT.md.

Contenido Obligatorio:

1. Guía de Despliegue (Deploy): Pasos para la plataforma elegida.

2. Auditoría Final de Trazabilidad: Tabla cruzada.

3. **Sincronización de Documentación:**

* Reescribe README.md para coincidir con el código final.

* Audita manuales obsoletos.

GIT CHECKPOINT (OBLIGATORIO):  
● git add docs/ README.md, git commit \-m "chore: deploy documentation and final closure"

CLÁUSULA DE FRENO:  
● Cierre final del ciclo.

**⚠️ PROMPT EXTRA: DEBUGGING Y FIXES**

Instrucción: Úsalo si algo sale mal o quieres cambiar algo.  
Tengo un problema o necesito un cambio.

**PASO 1: DIAGNÓSTICO**

* Si es error: Analiza logs, causas comunes (env, bridge, paths).

* Si es cambio: Análisis de Impacto (Docs, Código, Tests).

**PASO 2: EJECUCIÓN ATÓMICA**

* Aplica cambios archivo por archivo.

* Verifica Seguridad (claves, stateless).

* Actualiza Manuales.

* Actualiza docs/CHECKPOINT.md.

GIT CHECKPOINT:  
● git add ., git commit \-m "fix/refactor: \[descripción\]"

**🆘 PROMPT DE RECUPERACIÓN (RESUME)**

Instrucción: Copia esto si se reinicia el chat.  
¡HOLA\! He tenido un problema técnico.  
Por favor, lee el siguiente contenido de mi archivo de persistencia docs/CHECKPOINT.md:

\[PEGAR AQUÍ EL CONTENIDO DE TU ARCHIVO docs/CHECKPOINT.md\]

**TU TAREA:**

1. Analiza Fase y Archivo actual.

2. Identifica el siguiente paso.

3. Responde: "Contexto recuperado. Listo para \[Siguiente Paso\]. Di 'Adelante'."

