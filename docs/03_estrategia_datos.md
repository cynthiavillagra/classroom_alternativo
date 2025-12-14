# 💾 Estrategia de Datos — Classroom Explorer

> **Versión**: 1.0  
> **Fecha**: 2024-12-14  
> **Autor**: Equipo de Desarrollo  
> **Estado**: ✅ Aprobado

---

## 📑 Índice

1. [Decisión Arquitectónica](#1-decisión-arquitectónica)
2. [Justificación Técnica](#2-justificación-técnica)
3. [Implementación Actual](#3-implementación-actual)
4. [Roadmap Futuro](#4-roadmap-futuro)

---

## 1. Decisión Arquitectónica

### 1.1 Decisión: **NO usar base de datos propia (MVP)**

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DE DATOS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FUENTE DE DATOS: Google Classroom API (única fuente de verdad) │
│  PERSISTENCIA LOCAL: Ninguna (por ahora)                        │
│  CACHÉ: En memoria (runtime) - TTL: 5 minutos                   │
│  ESTADO: Stateless (cada request es independiente)              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Justificación Técnica

### 2.1 ¿Por Qué SÍ esta decisión?

| Razón | Explicación | Beneficio |
|-------|-------------|-----------|
| **Simplicidad** | No hay que gestionar migraciones, backups, sincronización | Menos complejidad, más foco en aprendizaje |
| **Datos siempre actualizados** | Leemos directo de Google Classroom | No hay problemas de sincronización |
| **Menos infraestructura** | Solo Vercel (serverless) | Sin costos de BD, sin mantenimiento |
| **Stateless** | Cada función Vercel es independiente | Escala automáticamente |
| **Prototipado rápido** | Podemos iterar sin preocuparnos por esquemas | MVP más rápido |
| **Educativo** | Aprendemos a trabajar con APIs externas | Patrón común en la industria |

---

### 2.2 ¿Por Qué NO usar BD (en este momento)?

#### ❌ Anti-Patrón: Duplicar Datos de Google

```
PROBLEMA:
Si guardamos cursos y materiales en nuestra BD:

1. SINCRONIZACIÓN:
   • ¿Qué pasa si el profesor borra un material en Classroom?
   • ¿Cómo detectamos cambios?
   • ¿Polling cada X minutos? (costoso)
   • ¿Webhooks? (Google Classroom no los tiene para todo)

2. CONSISTENCIA:
   • Nuestra BD puede quedar desactualizada
   • El usuario ve datos viejos
   • Necesitamos lógica compleja de "refresh"

3. COMPLEJIDAD:
   • Migraciones de esquema
   • Backups
   • Manejo de conflictos
   • Más código, más bugs potenciales

CONCLUSIÓN:
Para un MVP educativo, la complejidad NO vale la pena.
```

---

### 2.3 Trade-offs Aceptados

| Limitación | Impacto | Mitigación |
|------------|---------|------------|
| **Sin favoritos** | Usuario no puede marcar materiales | Futuro: agregar BD solo para esto |
| **Sin historial** | No guardamos búsquedas previas | Aceptable para MVP |
| **Sin offline** | Requiere conexión a internet | Aceptable (app web) |
| **Llamadas a API** | Cada request va a Google | Caché en memoria (5 min) |
| **Sin analytics** | No sabemos qué materiales son populares | Futuro: agregar tracking |

---

## 3. Implementación Actual

### 3.1 Flujo de Datos

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE LECTURA DE DATOS                    │
└─────────────────────────────────────────────────────────────────┘

1. Usuario hace request → GET /api/courses

2. Backend verifica caché en memoria:
   ┌─────────────────────────────────────┐
   │ ¿Hay cursos en caché?               │
   │ ¿Hace menos de 5 minutos?           │
   └─────────────────────────────────────┘
            │
            ├─ SÍ → Devolver desde caché (rápido)
            │
            └─ NO → Llamar a Google Classroom API
                    ↓
                    Obtener cursos
                    ↓
                    Guardar en caché (TTL: 5 min)
                    ↓
                    Devolver al usuario

3. Próximas requests (< 5 min) usan caché
   → Menos llamadas a Google API
   → Más rápido para el usuario
```

---

### 3.2 Implementación de Caché en Memoria

```python
# ═══════════════════════════════════════════════════════════════
# api/infrastructure/cache.py
# ═══════════════════════════════════════════════════════════════
from datetime import datetime, timedelta
from typing import Optional, Any

class MemoryCache:
    """
    Caché simple en memoria con TTL.
    
    POR QUÉ SÍ:
    • Reduce llamadas a Google API
    • Mejora performance
    • No requiere infraestructura externa
    
    POR QUÉ NO Redis/Memcached:
    • Overkill para MVP
    • Más infraestructura que gestionar
    • Vercel Serverless reinicia funciones (caché se pierde igual)
    
    LIMITACIÓN:
    • En Vercel, cada función tiene su propia memoria
    • El caché no se comparte entre requests
    • Aceptable para MVP (cada usuario tiene su caché)
    """
    
    def __init__(self):
        self._cache: dict[str, tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor del caché si no expiró.
        
        Args:
            key: Clave del caché
        
        Returns:
            Valor si existe y no expiró, None en caso contrario
        """
        if key not in self._cache:
            return None
        
        value, expiry = self._cache[key]
        
        if datetime.now() > expiry:
            # Expiró, eliminar
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """
        Guarda un valor en caché con TTL.
        
        Args:
            key: Clave del caché
            value: Valor a guardar
            ttl_seconds: Tiempo de vida en segundos (default: 5 min)
        """
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """Elimina una clave del caché."""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Limpia todo el caché."""
        self._cache.clear()


# Instancia global (singleton)
cache = MemoryCache()
```

---

### 3.3 Uso del Caché en Repository

```python
# ═══════════════════════════════════════════════════════════════
# api/infrastructure/repositories/google_classroom_repository.py
# ═══════════════════════════════════════════════════════════════
from api.infrastructure.cache import cache

class GoogleClassroomRepository:
    def get_user_courses(self, user_id: str) -> List[Course]:
        """
        Obtiene cursos del usuario con caché.
        
        ESTRATEGIA:
        1. Intentar obtener de caché
        2. Si no hay, llamar a Google API
        3. Guardar en caché para próximas requests
        """
        cache_key = f"courses_user_{user_id}"
        
        # 1. Intentar caché
        cached_courses = cache.get(cache_key)
        if cached_courses is not None:
            print(f"✅ Cache HIT: {cache_key}")
            return cached_courses
        
        print(f"❌ Cache MISS: {cache_key}")
        
        # 2. Llamar a Google API
        api_response = self.client.list_courses(access_token)
        
        # 3. Mapear a entidades
        courses = [
            self.mapper.api_course_to_domain(course_data)
            for course_data in api_response.get('courses', [])
        ]
        
        # 4. Guardar en caché (5 minutos)
        cache.set(cache_key, courses, ttl_seconds=300)
        
        return courses
```

---

## 4. Roadmap Futuro

### 4.1 Cuándo SÍ Agregar Base de Datos

```
┌─────────────────────────────────────────────────────────────────┐
│           SEÑALES PARA AGREGAR BASE DE DATOS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ AGREGAR BD SI:                                              │
│  • Necesitamos favoritos/marcadores persistentes                │
│  • Queremos analytics (materiales más vistos)                   │
│  • Necesitamos búsqueda full-text (indexar contenido)           │
│  • Queremos notificaciones (detectar nuevos materiales)         │
│  • El caché en memoria no es suficiente (muchos usuarios)       │
│                                                                 │
│  ❌ NO AGREGAR BD SI:                                           │
│  • Solo queremos duplicar datos de Google (anti-patrón)         │
│  • No hay features que lo justifiquen                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4.2 Propuesta de Esquema Futuro (Supabase)

Si en el futuro decidimos agregar BD, este sería el esquema **mínimo**:

```sql
-- ═══════════════════════════════════════════════════════════════
-- TABLA: users (perfil local del usuario)
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE users (
    id TEXT PRIMARY KEY,  -- Google User ID
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    picture_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════
-- TABLA: favorite_materials (materiales marcados como favoritos)
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE favorite_materials (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    material_id TEXT NOT NULL,  -- Google Material ID
    course_id TEXT NOT NULL,    -- Google Course ID
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, material_id)
);

CREATE INDEX idx_favorite_materials_user_id ON favorite_materials(user_id);

-- ═══════════════════════════════════════════════════════════════
-- TABLA: search_history (historial de búsquedas)
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    filters JSONB,  -- Filtros aplicados
    results_count INT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_search_history_user_id ON search_history(user_id);
CREATE INDEX idx_search_history_created_at ON search_history(created_at DESC);
```

**Nota:** Este esquema **NO se implementa ahora**. Solo está documentado para referencia futura.

---

### 4.3 Migración Futura

```
CUANDO DECIDAMOS AGREGAR BD:

1. Crear cuenta en Supabase (gratis hasta 500 MB)
2. Ejecutar el SQL del esquema
3. Agregar variables de entorno:
   - SUPABASE_URL
   - SUPABASE_ANON_KEY
4. Implementar Repository para Supabase
5. Usar Dependency Injection para elegir Repository
6. Mantener Google API como fuente de verdad
7. BD solo para features adicionales (favoritos, etc.)
```

---

## 📎 Resumen Ejecutivo

### Decisión Final

| Aspecto | Decisión |
|---------|----------|
| **Base de Datos** | ❌ No (por ahora) |
| **Fuente de Datos** | Google Classroom API |
| **Caché** | En memoria (TTL: 5 min) |
| **Persistencia** | Ninguna |
| **Estado** | Stateless |

### Ventajas

- ✅ Simplicidad arquitectónica
- ✅ Datos siempre actualizados
- ✅ Menos infraestructura
- ✅ Desarrollo más rápido

### Limitaciones Aceptadas

- ❌ Sin favoritos persistentes
- ❌ Sin historial de búsquedas
- ❌ Sin modo offline

### Próximo Paso

Pasar a la **Fase 4: Implementación del Código** (Domain Layer).

---

## ✅ Checklist de Aprobación

- [x] Decisión de no usar BD justificada
- [x] Estrategia de caché definida
- [x] Trade-offs documentados
- [x] Roadmap futuro claro
- [x] Listo para implementar código
