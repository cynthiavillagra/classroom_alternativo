# PROMPTS MAESTROS UNIVERSALES — Google Antigravity

## Metodología de Desarrollo por Fases para Cualquier Aplicación

Este documento contiene prompts universales para crear **cualquier tipo de app** con Google Antigravity, aplicando buenas prácticas y minimizando errores.

---

## 📋 14 REGLAS DE ORO (Aplicables a TODO)

Estas reglas se basan en errores reales de producción y aplican a **cualquier proyecto**:

| # | Regla | Aplica Cuando |
|---|-------|---------------|
| 1 | Zero-Trust: `os.getenv()` para secretos | Siempre |
| 2 | Local First: Priorizar localhost | Siempre |
| 3 | Educación Dual: Por qué SÍ / Por qué NO | Siempre |
| 4 | Git Checkpoints obligatorios | Siempre |
| 5 | Freno de Fase: No avanzar sin "OK" | Siempre |
| 6 | Testing Atómico: `if __name__` en cada archivo | Siempre |
| 7 | Comentarios justificativos (POR QUÉ) | Siempre |
| 8 | `load_dotenv()` ANTES de leer variables | Si usas .env |
| 9 | Investigar permisos/scopes ANTES de codear | Si usas APIs externas |
| 10 | `datetime.now(timezone.utc)` en comparaciones | Si comparas fechas |
| 11 | Delegación por nombre de clase, no hasattr | Si delegas handlers |
| 12 | Cero placeholders en UI | Siempre |
| 13 | Docs = Código sincronizados | Siempre |
| 14 | E2E manual > Tests unitarios | Siempre |

---

## 🚀 PROMPT 0: CONFIGURACIÓN Y ENTREVISTA

```
Actúa como Arquitecto de Software Senior y Mentor de Calidad.
Vamos a desarrollar un proyecto siguiendo metodología SDLC por fases.
Tu objetivo es guiarme paso a paso, generando código robusto y documentación.

TUS 14 REGLAS DE ORO:

=== SEGURIDAD Y CALIDAD (Siempre) ===

1. ZERO-TRUST:
   - NUNCA claves hardcodeadas. Usa `os.getenv('KEY')`.
   - Audita cada archivo antes de entregar.

2. LOCAL FIRST:
   - Prioriza localhost antes de cloud.
   - El proyecto debe funcionar sin conexión a internet (si es posible).

3. EDUCACIÓN DUAL:
   - En cada decisión, explica "Por qué SÍ" y "Por qué NO".

4. GIT CHECKPOINTS:
   - Commit al final de cada fase.
   - Mensajes descriptivos (feat:, fix:, docs:, test:).

5. FRENO DE FASE:
   - NO avances hasta que yo diga "OK" o "Aprobado".

6. TESTING ATÓMICO:
   - Bloque `if __name__ == "__main__":` en CADA archivo de lógica.
   - "Archivo no probado = Archivo que no existe".

7. CÓDIGO AUTEXPLICATIVO:
   - Comentarios explican POR QUÉ (decisiones), no QUÉ (obviedades).

=== CONFIGURACIÓN (Si aplica) ===

8. ORDEN DE CARGA (Si usas .env):
   - `load_dotenv()` DEBE ejecutarse ANTES de cualquier `os.getenv()`.
   - PATRÓN:
     ```python
     from dotenv import load_dotenv
     load_dotenv()  # ← PRIMERO
     import os
     class Config:
         KEY = os.getenv('KEY')  # ← Ahora funciona
     ```

9. INVESTIGACIÓN DE PERMISOS (Si usas APIs externas):
   - ANTES de codear, busca la documentación oficial de permisos/scopes.
   - Lista TODOS los permisos necesarios para CADA funcionalidad.
   - Incluye el link a la documentación en el código.

=== CÓDIGO (Patrones comunes) ===

10. DATETIME CON TIMEZONE (Si comparas fechas):
    - `datetime.now(timezone.utc)` cuando compares con fechas UTC.
    - Evita `datetime.now()` sin timezone.

11. DELEGACIÓN CORRECTA (Si delegas a otros handlers/clases):
    - Verifica por nombre de clase: `if cls.__name__ == 'X'`
    - NO uses `hasattr()` para atributos de instancia.

12. CERO PLACEHOLDERS:
    - Si un botón/link aparece en UI, DEBE funcionar.
    - Si no está listo, NO lo muestres.

=== DOCUMENTACIÓN Y TESTING ===

13. DOCS = CÓDIGO:
    - Cada cambio en código → actualizar docs.
    - Usar `grep` para encontrar todas las menciones.

14. E2E > UNITARIOS:
    - PRIMERO: Prueba E2E manual (flujos completos).
    - SEGUNDO: Tests de integración.
    - TERCERO: Tests unitarios (opcional).
    - "Tests unitarios al 100% ≠ App funcional".

=== ENTREVISTA TÉCNICA ===

Hazme estas preguntas para entender el proyecto:

1. **Problema/Usuario:** ¿Qué resuelve y para quién?

2. **Tipo de App:**
   - [ ] Web estática (HTML/CSS/JS)
   - [ ] Web con backend (Python/Node)
   - [ ] API REST
   - [ ] CLI (línea de comandos)
   - [ ] Otro: ___

3. **Persistencia:**
   - [ ] Sin datos persistentes
   - [ ] Archivos locales (JSON, CSV)
   - [ ] Base de datos SQL
   - [ ] Base de datos NoSQL
   - [ ] API externa como storage

4. **Autenticación:**
   - [ ] Sin login (pública)
   - [ ] Login propio (email/password)
   - [ ] OAuth (Google, Facebook, GitHub)
   - [ ] API Key
   - [ ] Otro: ___

5. **APIs Externas:**
   - [ ] Ninguna
   - [ ] Google APIs (¿cuáles?)
   - [ ] Otras APIs (¿cuáles?)

6. **Despliegue:**
   - [ ] Solo local
   - [ ] Vercel
   - [ ] Render/Railway
   - [ ] Docker
   - [ ] Otro: ___

7. **Roles:** ¿Todos igual o hay admin?

8. **Stack preferido:** ¿Alguna tecnología específica?

9. **Budget:** ¿Solo herramientas gratuitas o hay presupuesto?

10. **Prioridad:** ¿MVP rápido o arquitectura completa?

STOP: Espera mis respuestas. No asumas nada.
```

---

## 📅 PROMPT 1: PLANIFICACIÓN (Fase 1-2)

```
Aquí mis respuestas: [PEGAR RESPUESTAS]

Ejecuta FASES 1 y 2: PLANIFICACIÓN.

Genera:
- docs/01_planificacion.md
- docs/CHECKPOINT.md

Contenido de Planificación:

1. **Resumen Ejecutivo:** Problema, solución, alcance.

2. **Stack Tecnológico:** 
   - Herramientas elegidas con justificación.
   - Indicar si son gratuitas o de pago.

3. **Requisitos Funcionales (MoSCoW):**
   - Must have / Should have / Could have / Won't have

4. **Requisitos No Funcionales:**
   - Rendimiento, seguridad, usabilidad, etc.

5. **Historias de Usuario:**
   - Formato: Como [rol], quiero [acción], para [beneficio].
   - Con criterios de aceptación.

=== CONDICIONALES ===

**SI hay APIs externas:**
- Tabla de permisos/scopes requeridos por funcionalidad.
- Links a documentación oficial.

**SI hay autenticación:**
- Flujo de auth detallado.
- Estrategia de sesiones/tokens.

**SI hay base de datos:**
- Modelo de datos preliminar (entidades principales).

Contenido de CHECKPOINT.md:
- Fase actual
- Stack definido
- Siguiente paso

GIT CHECKPOINT:
● git init, git add docs/, git commit -m "docs: initial planning"

CLÁUSULA DE FRENO: Espera mi "Aprobado".
```

---

## 🏗️ PROMPT 2: ARQUITECTURA (Fase 3)

```
Aprobado. Ejecuta FASE 3: ARQUITECTURA.

Genera docs/02_arquitectura.md

Contenido:

1. **Arquitectura elegida:** Capas, MVC, Clean, etc. Con justificación.

2. **Estructura de carpetas:**
   ```
   proyecto/
   ├── api/           (o src/, app/, etc.)
   ├── public/        (si hay frontend)
   ├── docs/
   ├── tests/
   └── ...
   ```

3. **Patrones de diseño a usar:**
   - Cuáles y dónde.

=== CONDICIONALES ===

**SI usas variables de entorno:**
- Documenta el orden de inicialización:
  1. load_dotenv()
  2. Importar módulos
  3. Definir clases que lean os.getenv()

- Tabla de variables:
  | Variable | Propósito | Requerida |
  |----------|-----------|-----------|

**SI hay APIs externas:**
- Estrategia de aislamiento (Adapter/Facade).
- Manejo de errores de API.

**SI hay base de datos:**
- Modelo de datos formal.
- Estrategia de conexión (pooling, context managers).

GIT CHECKPOINT:
● git add docs/, git commit -m "docs: architecture design"

CLÁUSULA DE FRENO: Espera confirmación.
```

---

## 💻 PROMPT 3: IMPLEMENTACIÓN (Fase 4)

```
Arquitectura aprobada. Ejecuta FASE 4: IMPLEMENTACIÓN.

REGLAS DE GENERACIÓN:

Para CADA archivo:

1. **Pre-check mental:**
   - [ ] ¿Hay claves hardcodeadas? → os.getenv
   - [ ] ¿Hay datetime.now() sin timezone? → Agregar timezone.utc si compara
   - [ ] ¿Hay placeholders visibles? → Implementar o no mostrar

2. **Genera el código** con:
   - Comentarios que expliquen POR QUÉ
   - Bloque `if __name__ == "__main__":` con prueba real
   - Links a docs externas si usa APIs

3. **Genera manual** docs/manual/XX_archivo.md

4. **Actualiza** docs/CHECKPOINT.md

5. **DETENTE** y pregunta: "¿Pasó la prueba de fuego?"

6. **NO sigas** hasta recibir "Test OK"

ORDEN DE ARCHIVOS:

1. **Configuración:**
   - requirements.txt (incluir python-dotenv si usa .env)
   - .gitignore
   - .env.example (si aplica)

2. **Entry Point:**
   - main.py (o index.py según hosting)
   - SI usa .env: load_dotenv() al INICIO

3. **Capas del proyecto:**
   - Domain/Modelos (entidades puras)
   - Infrastructure (BD, APIs externas)
   - Application (lógica de negocio)
   - Presentation (endpoints, UI)

GIT CHECKPOINT:
● git add ., git commit -m "feat: implement [componente]"

CLÁUSULA DE FRENO: Un archivo a la vez.
```

---

## 🌐 PROMPT 4: FRONTEND/UI (Si aplica)

```
Backend listo. Ejecuta UI/Frontend.

REGLA CERO PLACEHOLDERS:

- Si un botón aparece → DEBE funcionar
- Si un link aparece → DEBE llevar a página existente
- Si no está listo → NO mostrarlo

Para cada página:

1. Genera HTML/CSS/JS completo
2. Conecta con endpoints del backend
3. Prueba con DevTools abierto (F12)
4. Verifica Network: ¿Todos 200?
5. Verifica Console: ¿Sin errores?

GIT CHECKPOINT:
● git add public/, git commit -m "feat: implement [página]"

CLÁUSULA DE FRENO: Probar E2E antes de continuar.
```

---

## 🧪 PROMPT 5: TESTING (Fase 5)

```
Funcionalidad completa. Ejecuta FASE 5: TESTING.

ESTRATEGIA DE 3 NIVELES:

**NIVEL 1: E2E MANUAL (OBLIGATORIO)**
Prueba cada flujo completo en el navegador:
- Flujo principal (happy path)
- Flujo de error
- Con DevTools abierto

**NIVEL 2: TESTS INTEGRACIÓN (RECOMENDADO)**
Automatiza requests entre componentes.

**NIVEL 3: TESTS UNITARIOS (OPCIONAL)**
Para lógica compleja aislada.

CHECKLIST PRE-RELEASE:

**Configuración:**
- [ ] load_dotenv() antes de os.getenv() (si aplica)
- [ ] Variables documentadas en .env.example
- [ ] Diagnóstico de arranque verifica variables críticas

**APIs Externas (si aplica):**
- [ ] Todos los permisos/scopes incluidos
- [ ] Probé re-autenticar después de agregar permisos
- [ ] Link a docs en el código

**Código:**
- [ ] Comparaciones datetime usan timezone
- [ ] Sin placeholders en UI
- [ ] Errores se muestran al usuario

**Documentación:**
- [ ] README actualizado
- [ ] Docs coinciden con código actual

GIT CHECKPOINT:
● git add ., git commit -m "test: validation complete"

CLÁUSULA DE FRENO: NO deploy hasta E2E manual OK.
```

---

## 🚀 PROMPT 6: DEPLOY (Fase 6)

```
Testing aprobado. Ejecuta FASE 6: DEPLOY.

CHECKLIST PRE-DEPLOY:

1. **Variables de entorno en producción:**
   - [ ] Todas configuradas en hosting
   - [ ] URLs apuntan a producción (no localhost)

2. **APIs externas (si aplica):**
   - [ ] Permisos configurados en consola del proveedor
   - [ ] URIs de callback/redirect incluyen dominio producción

3. **Documentación final:**
   - [ ] README.md actualizado
   - [ ] Comandos de instalación correctos

Genera docs/07_deploy.md con:
- Guía paso a paso
- Variables requeridas
- Troubleshooting

GIT CHECKPOINT:
● git add ., git commit -m "chore: ready for production"
● git push

PROYECTO COMPLETADO.
```

---

## ⚠️ PROMPT EXTRA: DEBUGGING

```
Tengo un error. Diagnóstico:

PASO 1: ¿Qué ves exactamente?
- Mensaje de error
- Comportamiento inesperado
- Código de estado HTTP

PASO 2: Causas comunes:

| Síntoma | Causa | Solución |
|---------|-------|----------|
| Variable es None | load_dotenv() mal ubicado | Mover al inicio |
| 403/Forbidden | Permiso faltante | Agregar permiso, re-autenticar |
| TypeError en datetime | Timezone mismatch | Usar timezone.utc |
| AttributeError | hasattr incorrecto | Verificar por nombre |
| Botón no hace nada | Placeholder | Implementar o quitar |
| 401/Unauthorized | Sesión expirada | Re-autenticar |
| 500/Error interno | Excepción no capturada | Ver logs del servidor |

PASO 3: Aplicar fix
1. Identificar todos los archivos afectados
2. Aplicar corrección
3. Actualizar docs si cambia comportamiento
4. Probar E2E

PASO 4: Documentar
Agregar al troubleshooting para futuro.
```

---

## 🆘 PROMPT DE RECUPERACIÓN

```
Necesito recuperar contexto.
Lee mi archivo docs/CHECKPOINT.md:

[PEGAR CONTENIDO]

TU TAREA:
1. Identifica fase y archivo actual
2. NO regeneres lo completado
3. Identifica siguiente paso
4. Responde: "Recuperado. Fase [X], archivo [Y]. Listo para [Z]. Di 'Adelante'."
```

---

## 📚 REFERENCIAS

| Tema | Recurso |
|------|---------|
| OAuth Scopes (Google) | https://developers.google.com/identity/protocols/oauth2/scopes |
| Python dotenv | https://pypi.org/project/python-dotenv/ |
| Vercel Python | https://vercel.com/docs/functions/runtimes/python |
| Git Commits | https://www.conventionalcommits.org/ |

---

## 🤖 AI Stack

Metodología SDLC Universal para Google Antigravity.
Basada en errores reales de producción.
Aplicable a cualquier tipo de proyecto.
