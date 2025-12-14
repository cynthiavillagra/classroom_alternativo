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

from datetime import datetime
from typing import Dict, Any, Optional
from api.domain.entities import Course, Material, MaterialType, CourseState
from api.domain.factories import CourseFactory, MaterialFactory


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
        
        Args:
            api_data: Respuesta de la API de Google
            course_id: ID del curso al que pertenece
        
        Returns:
            Material: Entidad de dominio
        """
        # Detectar tipo de material
        material_type = self._detect_material_type(api_data)
        
        # Extraer URL del material
        url = self._extract_material_url(api_data, material_type)
        
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
            'created_at': created_at.isoformat(),
            'updated_at': updated_at.isoformat(),
            'due_date': due_date.isoformat() if due_date else None,
            'max_points': api_data.get('maxPoints')
        })
    
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
        Extrae la URL del material.
        
        Args:
            api_data: Datos de la API
            material_type: Tipo detectado
        
        Returns:
            URL del material
        """
        # URL alternativa (link al courseWork en Classroom)
        alternate_link = api_data.get('alternateLink', '')
        
        materials = api_data.get('materials', [])
        if not materials:
            return alternate_link
        
        first_material = materials[0]
        
        # Extraer URL según tipo
        if 'driveFile' in first_material:
            drive_file = first_material['driveFile'].get('driveFile', {})
            return drive_file.get('alternateLink', alternate_link)
        
        if 'youtubeVideo' in first_material:
            video_id = first_material['youtubeVideo'].get('id', '')
            return f"https://www.youtube.com/watch?v={video_id}"
        
        if 'link' in first_material:
            return first_material['link'].get('url', alternate_link)
        
        if 'form' in first_material:
            return first_material['form'].get('formUrl', alternate_link)
        
        return alternate_link
    
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
            datetime o None
        """
        try:
            return datetime(
                year=due_date.get('year', 2024),
                month=due_date.get('month', 1),
                day=due_date.get('day', 1),
                hour=due_time.get('hours', 23),
                minute=due_time.get('minutes', 59)
            )
        except (ValueError, TypeError):
            return None
