# 📄 Courses Handler — Manual Técnico

**Archivo:** `api/routes/courses.py`  
**Propósito:** Endpoints para listar cursos usando Python POO puro  
**Trazabilidad:** RF-M02 (Listar cursos), CU-002, HU-002

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — Importar dependencias:**
   - `http.server.BaseHTTPRequestHandler`: Clase base HTTP
   - `ListUserCourses`: Use Case del Application Layer
   - `GoogleClassroomRepository`: Implementación del repositorio
   - `session_store`: Sesiones de auth.py
   - POR QUÉ reutilizar Use Cases: No duplicar lógica

2. **Paso 2 — Clase CoursesHandler (herencia POO):**
   - Hereda de `BaseHTTPRequestHandler`
   - Constructor con Dependency Injection
   - POR QUÉ DI en constructor: Testeable, desacoplado

3. **Paso 3 — Método do_GET (router):**
   - Parsea path y query string
   - Router manual basado en path
   - POR QUÉ manual: Sin framework de routing

4. **Paso 4 — Ruta /api/courses:**
   - Verifica autenticación (session_store)
   - Parsea query params (include_archived, state)
   - Crea Request DTO
   - Ejecuta Use Case
   - Serializa respuesta con to_dict()

5. **Paso 5 — Ruta /api/courses/{id}:**
   - Extrae course_id del path
   - Llama a repository.get_course_by_id()
   - Maneja errores como 404

6. **Paso 6 — Métodos helper:**
   - `_send_json_response()`: Respuesta JSON con CORS
   - `_get_session_id_from_cookie()`: Reutilizado de auth

---

## 🎓 Aclaración Metodológica: Rol del Bloque Main

*Este bloque valida que la clase POO está correctamente definida y que usa los Use Cases. No levanta servidor HTTP ni hace llamadas reales a Google.*

---

## 📝 Código Clave (Fragmento)

```python
# ═══════════════════════════════════════════════════════════════
# Paso 2: Handler HTTP para cursos (herencia POO)
# ═══════════════════════════════════════════════════════════════
class CoursesHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        # Dependency Injection
        self.repository = GoogleClassroomRepository()
        self.list_courses_use_case = ListUserCourses(self.repository)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/courses':
            self._handle_list_courses(query)
        elif path.startswith('/api/courses/'):
            course_id = path.split('/')[-1]
            self._handle_get_course(course_id)
    
    def _handle_list_courses(self, query):
        # Verificar autenticación
        access_token = session_store.get(session_id, 'access_token')
        
        # Crear request DTO
        request = ListUserCoursesRequest(...)
        
        # Ejecutar Use Case
        response = self.list_courses_use_case.execute(request)
        
        # Serializar
        courses_json = [c.to_dict() for c in response.courses]
        self._send_json_response({'courses': courses_json})
```

---

## 🔥 Prueba de Fuego

### Comando Exacto
```powershell
python -m api.routes.courses
```

### Salida Esperada
```
============================================================
PRUEBAS ATÓMICAS: Courses Handler (Python POO puro)
============================================================

1. Verificar CoursesHandler (herencia POO):
   ✓ Clase: CoursesHandler
   ✓ Hereda de: BaseHTTPRequestHandler
   ✓ Método do_GET: True

3. Verificar integración con Application Layer:
   ✓ ListUserCourses importado: True

4. Verificar que es Python puro (sin Flask):
   ✓ Flask en sys.modules: False
   ✓ ¡Confirmado: NO usa Flask!

✅ Prueba de Courses Handler (POO puro): OK
============================================================
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ reutilizar Use Cases

| Beneficio | Explicación |
|-----------|-------------|
| **DRY** | No duplicamos lógica de negocio |
| **Tested** | Use Case ya tiene prueba atómica |
| **Desacoplado** | Handler solo hace HTTP, Use Case hace lógica |
| **Reutilizable** | Misma lógica para CLI, API, etc. |

### ❌ POR QUÉ NO poner lógica en el Handler

| Problema | Impacto |
|----------|---------|
| **Duplicación** | Si cambia la lógica, hay que cambiar en varios lugares |
| **No testeable** | Hay que levantar HTTP para testear lógica |
| **Fat handlers** | Handlers con cientos de líneas |

---

## 🎓 Conceptos Educativos

### Integración de Capas

```
HTTP Request
    ↓
CoursesHandler (API Layer)
    ↓
ListUserCourses (Application Layer)
    ↓
GoogleClassroomRepository (Infrastructure Layer)
    ↓
Google Classroom API
```

Cada capa tiene una responsabilidad clara.

### Dependency Injection en Handler

```python
def __init__(self, *args, **kwargs):
    # El handler CREA sus dependencias
    self.repository = GoogleClassroomRepository()
    self.list_courses_use_case = ListUserCourses(self.repository)
```

Esto podría mejorarse con un contenedor de DI, pero para MVP es suficiente.
