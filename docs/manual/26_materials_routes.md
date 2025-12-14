# Manual Técnico: materials.py

## Propósito

**Trazabilidad Completa:**
* **Módulo:** API Layer - Materials Handler
* **Historia de Usuario:** HU-003 (Como docente, quiero listar materiales de un curso)
* **Criterio de Aceptación:** CA-003.1 (Listar materiales con filtros)

---

## Estrategia de Construcción Incremental

1. **Validación de Dependencias:**
   - `http.server.BaseHTTPRequestHandler`: Clase base HTTP de Python estándar
   - `ListCourseMaterials`: Use Case del Application Layer
   - `MaterialType`: Enum del Domain Layer para filtrar por tipo
   - POR QUÉ no Flask: Requisito de Python POO puro sin frameworks

2. **Estructura Base:**
   - Clase `MaterialsHandler` hereda de `BaseHTTPRequestHandler`
   - Constructor con Dependency Injection del repositorio
   - Método `do_GET()` como punto de entrada HTTP

3. **Lógica Nuclear:**
   - Parsear path para extraer `course_id`
   - Verificar autenticación desde `session_store`
   - Parsear query params: `type`, `q` (search), `limit`
   - Crear Request DTO y ejecutar Use Case
   - Serializar respuesta a JSON

---

## Aclaración Metodológica: Rol del Bloque Main

*Este bloque es una herramienta de construcción. Sirve para validar que el archivo funciona en aislamiento (Prueba Atómica) antes de conectarlo al sistema. No reemplaza a los tests unitarios formales de la Fase 5.*

---

## Código Fuente (Fragmento Clave)

```python
class MaterialsHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        # Dependency Injection
        self.repository = GoogleClassroomRepository()
        self.list_materials_use_case = ListCourseMaterials(self.repository)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        # Router: /api/courses/{course_id}/materials
        if '/materials' in path:
            course_id = parts[3]
            self._handle_list_materials(course_id, query)
    
    def _handle_list_materials(self, course_id, query):
        # Verificar autenticación
        access_token = session_store.get(session_id, 'access_token')
        
        # Parsear filtros
        filter_type = MaterialType.from_string(query.get('type'))
        
        # Ejecutar Use Case
        request = ListCourseMaterialsRequest(...)
        response = self.list_materials_use_case.execute(request)
        
        # Serializar
        self._send_json_response({
            'materials': [m.to_dict() for m in response.materials],
            'type_counts': response.type_counts
        })
```

---

## Prueba de Fuego (Unit Test Rápido)

1. Ejecuta: `python -m api.routes.materials`
2. Verifica que imprima:
```
✅ Prueba de Materials Handler (POO puro): OK
```

---

## Análisis Dual

### Por qué SÍ:
- **Reutiliza Use Cases**: No duplicamos lógica de filtrado/búsqueda
- **POO pura**: Sin dependencias de frameworks externos
- **REST-compliant**: Sigue convención `/courses/{id}/materials`
- **Filtros flexibles**: type, search, limit ya implementados en Use Case

### Por qué NO (riesgos de hacerlo mal):
- **Sin Use Case**: Duplicar lógica de filtrado en el handler
- **Sin validación**: Aceptar cualquier tipo sin verificar enum
- **Sin auth check**: Exponer datos sin verificar sesión
