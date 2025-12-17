"""
Classroom Mapper - Classroom Explorer

Adapter que convierte respuestas de Google Classroom API a entidades de dominio.

POR QUÉ SÍ usar Mapper (Adapter Pattern):
✅ Aísla los cambios de la API externa
✅ Convierte formatos externos a formatos internos
✅ Si Google cambia su API, solo cambiamos este archivo
✅ El dominio no sabe nada de Google

POR QUÉ NO convertir directamente en el repositorio:
❌ Mezcla responsabilidades (HTTP + conversión)
❌ Código difícil de testear
❌ Si cambia la API, hay que cambiar mucho código
"""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Importar dependencias
# ═══════════════════════════════════════════════════════════════
# POR QUÉ datetime: Para parsear timestamps de Google
# POR QUÉ Factories: Para crear entidades válidas
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from src.domain.entities import Course, Material, MaterialType, CourseState
from src.domain.factories import CourseFactory, MaterialFactory


# ═══════════════════════════════════════════════════════════════
# Paso 2: Definir el Mapper (Adapter Pattern)
# ═══════════════════════════════════════════════════════════════
# POR QUÉ Adapter: Aísla cambios de API externa del dominio
class ClassroomMapper:
    """
    Mapper para convertir respuestas de Google Classroom API a entidades de dominio.
    
    Este es el ÚNICO lugar donde conocemos la estructura de la API de Google.
    El resto del código trabaja con entidades de dominio limpias.
    """
    
    def api_course_to_domain(self, api_data: Dict[str, Any]) -> Course:
        """
        Convierte un curso de la API de Google a entidad Course.
        
        Args:
            api_data: Respuesta de la API de Google (diccionario)
        
        Returns:
            Course: Entidad de dominio
        
        Example API response:
            {
                "id": "123456789",
                "name": "Matemáticas 3°A",
                "section": "Turno Mañana",
                "descriptionHeading": "Bienvenidos al curso",
                "description": "Curso de matemáticas...",
                "ownerId": "987654321",
                "creationTime": "2024-01-15T10:00:00.000Z",
                "updateTime": "2024-12-01T15:30:00.000Z",
                "courseState": "ACTIVE"
            }
        """
        # Mapear campos de Google API a nuestro formato
        return CourseFactory.create_from_dict({
            'id': api_data.get('id', ''),
            'name': api_data.get('name', 'Sin nombre'),
            'section': api_data.get('section'),
            'description': api_data.get('description') or api_data.get('descriptionHeading'),
            'state': api_data.get('courseState', 'ACTIVE'),
            'owner_id': api_data.get('ownerId', ''),
            'created_at': api_data.get('creationTime', datetime.now().isoformat()),
            'updated_at': api_data.get('updateTime', datetime.now().isoformat())
        })
    
    def api_material_to_domain(
        self,
        api_data: Dict[str, Any],
        course_id: str
    ) -> Material:
        """
        Convierte un material de la API de Google a entidad Material.
        
        Maneja tanto courseWork como courseWorkMaterials.
        [FIX v1.0.2] Ahora extrae TODOS los adjuntos, no solo el primero.
        
        Args:
            api_data: Respuesta de la API de Google
            course_id: ID del curso al que pertenece
        
        Returns:
            Material: Entidad de dominio
        """
        # Detectar tipo de material
        material_type = self._detect_material_type(api_data)
        
        # Extraer URL principal del material
        url = self._extract_material_url(api_data, material_type)
        
        # [FIX v1.0.2] Extraer TODOS los adjuntos
        attachments = self._extract_all_attachments(api_data)
        
        # Extraer fechas
        created_at = self._parse_google_timestamp(
            api_data.get('creationTime', datetime.now().isoformat())
        )
        updated_at = self._parse_google_timestamp(
            api_data.get('updateTime', datetime.now().isoformat())
        )
        
        # Extraer due_date si es una tarea
        due_date = None
        if 'dueDate' in api_data and 'dueTime' in api_data:
            due_date = self._parse_due_date(api_data['dueDate'], api_data['dueTime'])
        
        return MaterialFactory.create_from_dict({
            'id': api_data.get('id', ''),
            'course_id': course_id,
            'title': api_data.get('title', 'Sin título'),
            'description': api_data.get('description'),
            'type': material_type.value,
            'url': url,
            'attachments': attachments,
            'created_at': created_at.isoformat(),
            'updated_at': updated_at.isoformat(),
            'due_date': due_date.isoformat() if due_date else None,
            'max_points': api_data.get('maxPoints')
        })
    
    def api_announcement_to_domain(
        self,
        api_data: Dict[str, Any],
        course_id: str
    ) -> Material:
        """
        Convierte un anuncio (announcement) de la API de Google a entidad Material.
        
        Args:
            api_data: Respuesta de la API de Google (announcement)
            course_id: ID del curso al que pertenece
        
        Returns:
            Material: Entidad de dominio con tipo ANNOUNCEMENT
        """
        # Los anuncios tienen texto en 'text' en lugar de 'title'
        text = api_data.get('text', 'Sin contenido')
        # Tomar las primeras 100 caracteres como título
        title = text[:100] + '...' if len(text) > 100 else text
        
        # [FIX] Obtener alternateLink primero (link directo al anuncio)
        alternate_link = api_data.get('alternateLink', '')
        announcement_id = api_data.get('id', '')
        
        # Extraer URL del primer material adjunto si existe
        url = ''
        materials_data = api_data.get('materials', [])
        if materials_data:
            url = self._extract_single_material_url(materials_data[0])
        
        # [FIX] Fallback robusto para URL
        if not url:
            # Usar alternateLink si está disponible
            url = alternate_link
        if not url:
            # Generar URL directa al curso en Classroom
            url = f"https://classroom.google.com/c/{course_id}"
            if announcement_id:
                url = f"https://classroom.google.com/c/{course_id}/p/{announcement_id}"
        
        # Extraer fechas
        created_at = self._parse_google_timestamp(
            api_data.get('creationTime', datetime.now().isoformat())
        )
        updated_at = self._parse_google_timestamp(
            api_data.get('updateTime', datetime.now().isoformat())
        )
        
        return MaterialFactory.create_from_dict({
            'id': api_data.get('id', ''),
            'course_id': course_id,
            'title': title,
            'description': text,  # El texto completo va en description
            'type': MaterialType.ANNOUNCEMENT.value,
            'url': url,
            'created_at': created_at.isoformat(),
            'updated_at': updated_at.isoformat(),
            'due_date': None,
            'max_points': None
        })
    
    def _extract_single_material_url(self, material_data: Dict[str, Any]) -> str:
        """
        Extrae URL de un solo material adjunto.
        
        [FIX] Maneja ambas estructuras de driveFile:
        - Directa: driveFile.alternateLink
        - Anidada: driveFile.driveFile.alternateLink
        """
        if 'driveFile' in material_data:
            drive_data = material_data.get('driveFile', {})
            # Intentar estructura directa primero
            url = drive_data.get('alternateLink', '')
            if not url:
                # Intentar estructura anidada
                url = drive_data.get('driveFile', {}).get('alternateLink', '')
            return url
        if 'youtubeVideo' in material_data:
            video_id = material_data['youtubeVideo'].get('id', '')
            if video_id:
                return f"https://youtube.com/watch?v={video_id}"
            return material_data['youtubeVideo'].get('alternateLink', '')
        if 'link' in material_data:
            return material_data['link'].get('url', '')
        if 'form' in material_data:
            return material_data['form'].get('formUrl', '')
        return ''
    
    def _extract_all_attachments(self, api_data: Dict[str, Any]) -> list:
        """
        [FIX v1.0.2] Extrae TODOS los adjuntos de un material.
        
        Un material de Google Classroom puede tener múltiples adjuntos:
        - Varios PDFs
        - Links + Videos
        - Formularios + Documentos
        
        Returns:
            Lista de adjuntos, cada uno con {type, title, url}
        """
        attachments = []
        materials_list = api_data.get('materials', [])
        
        for material in materials_list:
            attachment = self._parse_single_attachment(material)
            if attachment and attachment.get('url'):
                attachments.append(attachment)
        
        return attachments
    
    def _parse_single_attachment(self, material_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Parsea un solo attachment y devuelve sus datos.
        
        Returns:
            Dict con {type, title, url} o {} si no es válido
        """
        if 'driveFile' in material_data:
            drive_data = material_data.get('driveFile', {})
            inner = drive_data.get('driveFile', drive_data)
            return {
                'type': 'file',
                'title': inner.get('title', 'Archivo'),
                'url': inner.get('alternateLink', drive_data.get('alternateLink', ''))
            }
        
        if 'youtubeVideo' in material_data:
            video_data = material_data.get('youtubeVideo', {})
            video_id = video_data.get('id', '')
            return {
                'type': 'video',
                'title': video_data.get('title', 'Video'),
                'url': f"https://youtube.com/watch?v={video_id}" if video_id else video_data.get('alternateLink', '')
            }
        
        if 'link' in material_data:
            link_data = material_data.get('link', {})
            return {
                'type': 'link',
                'title': link_data.get('title', 'Enlace'),
                'url': link_data.get('url', '')
            }
        
        if 'form' in material_data:
            form_data = material_data.get('form', {})
            return {
                'type': 'form',
                'title': form_data.get('title', 'Formulario'),
                'url': form_data.get('formUrl', '')
            }
        
        return {}
    
    def _detect_material_type(self, api_data: Dict[str, Any]) -> MaterialType:
        """
        Detecta el tipo de material basándose en la estructura de la API.
        
        Google Classroom tiene diferentes estructuras para diferentes tipos:
        - courseWork: Tareas, quizzes
        - courseWorkMaterials: Materiales de referencia
        
        Los materiales pueden tener:
        - materials[].driveFile → PDF, DOC, etc.
        - materials[].youtubeVideo → VIDEO
        - materials[].link → LINK
        - materials[].form → FORM
        """
        # Si tiene workType, es una tarea
        work_type = api_data.get('workType', '')
        if work_type == 'ASSIGNMENT':
            return MaterialType.ASSIGNMENT
        
        # Buscar en materials[]
        materials = api_data.get('materials', [])
        if not materials:
            return MaterialType.FILE
        
        first_material = materials[0]
        
        # Detectar por tipo de adjunto
        if 'driveFile' in first_material:
            drive_file = first_material['driveFile']
            mime_type = drive_file.get('driveFile', {}).get('mimeType', '')
            return self._mime_to_material_type(mime_type)
        
        if 'youtubeVideo' in first_material:
            return MaterialType.VIDEO
        
        if 'link' in first_material:
            return MaterialType.LINK
        
        if 'form' in first_material:
            return MaterialType.FORM
        
        return MaterialType.FILE
    
    def _mime_to_material_type(self, mime_type: str) -> MaterialType:
        """
        Convierte MIME type a MaterialType.
        
        Args:
            mime_type: MIME type del archivo
        
        Returns:
            MaterialType correspondiente
        """
        mime_mapping = {
            'application/pdf': MaterialType.PDF,
            'application/vnd.google-apps.document': MaterialType.DOCUMENT,
            'application/vnd.google-apps.presentation': MaterialType.DOCUMENT,
            'application/vnd.google-apps.spreadsheet': MaterialType.DOCUMENT,
            'application/vnd.google-apps.form': MaterialType.FORM,
            'image/': MaterialType.IMAGE,
            'video/': MaterialType.VIDEO,
        }
        
        for prefix, material_type in mime_mapping.items():
            if mime_type.startswith(prefix):
                return material_type
        
        return MaterialType.FILE
    
    def _extract_material_url(
        self,
        api_data: Dict[str, Any],
        material_type: MaterialType
    ) -> str:
        """
        Extrae la URL del material con fallback robusto.
        
        IMPORTANTE: Siempre debe retornar una URL válida.
        Si no hay URL específica, usa alternateLink.
        Si tampoco hay alternateLink, genera URL directa a Classroom.
        
        Args:
            api_data: Datos de la API
            material_type: Tipo detectado
        
        Returns:
            URL del material (nunca vacía)
        """
        # Obtener IDs para fallback a URL de Classroom
        course_id = api_data.get('courseId', '')
        material_id = api_data.get('id', '')
        
        # URL alternativa (link al courseWork en Classroom)
        alternate_link = api_data.get('alternateLink', '')
        
        # URL de fallback final: directo a Google Classroom
        # [FIX] Generar URL válida si no hay alternateLink
        fallback_url = alternate_link
        if not fallback_url and course_id:
            # Generar URL directa a Classroom
            fallback_url = f"https://classroom.google.com/c/{course_id}"
            if material_id:
                # Añadir ID del material si está disponible
                fallback_url = f"https://classroom.google.com/c/{course_id}/a/{material_id}/details"
        
        # Si aún no hay URL, usar URL genérica de Classroom
        if not fallback_url:
            fallback_url = "https://classroom.google.com"
        
        materials = api_data.get('materials', [])
        if not materials:
            return fallback_url
        
        first_material = materials[0]
        
        # Extraer URL según tipo
        if 'driveFile' in first_material:
            # [FIX] Estructura correcta de driveFile en la API
            drive_file_data = first_material.get('driveFile', {})
            # La URL puede estar directamente o en un sub-objeto driveFile
            url = drive_file_data.get('alternateLink', '')
            if not url:
                inner_drive = drive_file_data.get('driveFile', {})
                url = inner_drive.get('alternateLink', '')
            return url if url else fallback_url
        
        if 'youtubeVideo' in first_material:
            video_data = first_material.get('youtubeVideo', {})
            video_id = video_data.get('id', '')
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"
            # Fallback a alternateLink del video
            return video_data.get('alternateLink', fallback_url)
        
        if 'link' in first_material:
            link_url = first_material['link'].get('url', '')
            return link_url if link_url else fallback_url
        
        if 'form' in first_material:
            form_url = first_material['form'].get('formUrl', '')
            return form_url if form_url else fallback_url
        
        return fallback_url
    
    def _parse_google_timestamp(self, timestamp: str) -> datetime:
        """
        Parsea un timestamp de Google (ISO 8601 con Z).
        
        Args:
            timestamp: String en formato ISO 8601
        
        Returns:
            datetime object
        """
        if not timestamp:
            return datetime.now()
        
        # Remover 'Z' y agregar timezone
        timestamp = timestamp.replace('Z', '+00:00')
        
        try:
            return datetime.fromisoformat(timestamp)
        except ValueError:
            return datetime.now()
    
    def _parse_due_date(
        self,
        due_date: Dict[str, int],
        due_time: Dict[str, int]
    ) -> Optional[datetime]:
        """
        Parsea fecha y hora de entrega de Google.
        
        Args:
            due_date: {"year": 2024, "month": 12, "day": 15}
            due_time: {"hours": 23, "minutes": 59}
        
        Returns:
            datetime o None (con timezone UTC para consistencia)
        """
        from datetime import timezone
        
        try:
            dt = datetime(
                year=due_date.get('year', 2024),
                month=due_date.get('month', 1),
                day=due_date.get('day', 1),
                hour=due_time.get('hours', 23),
                minute=due_time.get('minutes', 59),
                tzinfo=timezone.utc  # Agregar timezone UTC
            )
            return dt
        except (ValueError, TypeError):
            return None


# ═══════════════════════════════════════════════════════════════
# PRUEBAS ATÓMICAS
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    """
    Pruebas rápidas para verificar que ClassroomMapper funciona.
    
    Ejecutar con:
        python -m api.infrastructure.mappers.classroom_mapper
    """
    print("=" * 60)
    print("PRUEBAS ATÓMICAS: ClassroomMapper")
    print("=" * 60)
    
    mapper = ClassroomMapper()
    
    # Test 1: Convertir curso de API a dominio
    print("\n1. Convertir curso de API a dominio:")
    api_course = {
        "id": "123456789",
        "name": "Matemáticas 3°A",
        "section": "Turno Mañana",
        "description": "Curso de matemáticas",
        "ownerId": "987654321",
        "creationTime": "2024-01-15T10:00:00.000Z",
        "updateTime": "2024-12-01T15:30:00.000Z",
        "courseState": "ACTIVE"
    }
    course = mapper.api_course_to_domain(api_course)
    print(f"   ✓ Curso convertido: {course}")
    print(f"   ✓ ID: {course.id}")
    print(f"   ✓ State: {course.state}")
    
    # Test 2: Detectar tipo ASSIGNMENT
    print("\n2. Detectar tipo ASSIGNMENT:")
    api_assignment = {"workType": "ASSIGNMENT"}
    detected = mapper._detect_material_type(api_assignment)
    print(f"   ✓ Tipo detectado: {detected} (esperado: ASSIGNMENT)")
    
    # Test 3: Detectar tipo VIDEO
    print("\n3. Detectar tipo VIDEO:")
    api_video = {"materials": [{"youtubeVideo": {"id": "abc123"}}]}
    detected = mapper._detect_material_type(api_video)
    print(f"   ✓ Tipo detectado: {detected} (esperado: VIDEO)")
    
    # Test 4: Detectar tipo LINK
    print("\n4. Detectar tipo LINK:")
    api_link = {"materials": [{"link": {"url": "https://example.com"}}]}
    detected = mapper._detect_material_type(api_link)
    print(f"   ✓ Tipo detectado: {detected} (esperado: LINK)")
    
    # Test 5: Detectar tipo PDF por MIME
    print("\n5. Detectar PDF por MIME type:")
    detected = mapper._mime_to_material_type("application/pdf")
    print(f"   ✓ Tipo detectado: {detected} (esperado: PDF)")
    
    # Test 6: Extraer URL de YouTube
    print("\n6. Extraer URL de YouTube:")
    url = mapper._extract_material_url(api_video, MaterialType.VIDEO)
    print(f"   ✓ URL extraída: {url}")
    
    # Test 7: Parsear timestamp de Google
    print("\n7. Parsear timestamp de Google:")
    timestamp = "2024-01-15T10:00:00.000Z"
    parsed = mapper._parse_google_timestamp(timestamp)
    print(f"   ✓ Timestamp parseado: {parsed}")
    print(f"   ✓ Tipo: {type(parsed).__name__}")
    
    # Test 8: Parsear due_date de Google
    print("\n8. Parsear due_date de Google:")
    due_date = {"year": 2024, "month": 12, "day": 20}
    due_time = {"hours": 23, "minutes": 59}
    parsed_due = mapper._parse_due_date(due_date, due_time)
    print(f"   ✓ Due date parseada: {parsed_due}")
    
    # Test 9: Convertir material completo
    print("\n9. Convertir material de API a dominio:")
    api_material = {
        "id": "mat_123",
        "title": "Tarea 1: Ejercicios",
        "description": "Resolver los ejercicios",
        "workType": "ASSIGNMENT",
        "alternateLink": "https://classroom.google.com/c/123",
        "creationTime": "2024-01-15T10:00:00.000Z",
        "updateTime": "2024-12-01T15:30:00.000Z",
        "dueDate": {"year": 2024, "month": 12, "day": 20},
        "dueTime": {"hours": 23, "minutes": 59},
        "maxPoints": 100
    }
    material = mapper.api_material_to_domain(api_material, "course_456")
    print(f"   ✓ Material convertido: {material}")
    print(f"   ✓ Tipo: {material.type}")
    print(f"   ✓ Max points: {material.max_points}")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de ClassroomMapper: OK")
    print("=" * 60)
