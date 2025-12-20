# Manual Técnico: materials.html (Frontend)

## Propósito

**Trazabilidad Completa:**
* **Módulo:** Presentation Layer - Materials View (Frontend)
* **Historia de Usuario:** HU-003 (Como docente, quiero listar materiales de un curso)
* **Criterio de Aceptación:** CA-003.2 (Visualizar materiales con filtros y descarga)

---

## Estructura del Archivo

```
public/materials.html
├── HEAD: Meta, estilos externos
├── BODY:
│   ├── Header (navegación)
│   ├── Main:
│   │   ├── Course Header (título del curso)
│   │   ├── Filters Bar (búsqueda, tipos, toggle vista)
│   │   └── Materials Container (cards o tabla)
│   └── Footer
├── STYLE: CSS embebido para materiales
└── SCRIPT: Lógica JavaScript
```

---

## Componentes Principales

### 1. Sistema de Filtros (v1.0.4)

```javascript
// Variables de estado
let currentFilterType = '';   // Tipo actual (video, pdf, etc.)
let currentSearchQuery = '';  // Texto de búsqueda

// Cargar materiales con filtros
async function loadMaterials(filterType = '', searchQuery = '') {
    let url = `/api/courses/${courseId}/materials`;
    const params = new URLSearchParams();
    
    if (filterType) params.set('type', filterType);
    if (searchQuery) params.set('q', searchQuery.trim());
    
    // Fetch y render...
}
```

**Tipos de filtro disponibles:**
| Botón | Tipo | Icono |
|-------|------|-------|
| Todos | `""` | 📚 |
| Videos | `video` | 🎬 |
| PDFs | `pdf` | 📄 |
| Notebooks | `notebook` | 📓 |
| Links | `link` | 🔗 |
| Documentos | `document` | 📝 |
| Formularios | `form` | 📋 |
| Tareas | `assignment` | ✏️ |

---

### 2. Toggle de Vista (v1.0.8)

```javascript
let currentView = 'cards';  // 'cards' o 'list'
let cachedMaterials = [];   // Materiales cacheados para cambio de vista

function applyCurrentView(materials) {
    cachedMaterials = materials;
    const container = document.getElementById('materialsContainer');
    
    if (currentView === 'list') {
        container.classList.add('view-list');
        container.innerHTML = renderListView(materials);
    } else {
        container.classList.remove('view-list');
        container.innerHTML = renderCardsView(materials);
    }
}
```

**Vistas disponibles:**
| Vista | Descripción |
|-------|-------------|
| 🃏 **Cards** | Tarjetas individuales por material |
| 📋 **Lista** | Tabla plana donde cada recurso es una fila |

---

### 3. Sistema de Descarga Directa (v1.0.9)

#### Función `getDownloadUrl()`

Convierte URLs de Google a formato de descarga directa:

```javascript
function getDownloadUrl(url) {
    if (!url) return '';
    
    // Google Drive: /file/d/{id}/view → /uc?export=download&id={id}
    const driveFileMatch = url.match(/drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)/);
    if (driveFileMatch) {
        return `https://drive.google.com/uc?export=download&id=${driveFileMatch[1]}`;
    }
    
    // Google Docs → PDF
    if (url.includes('docs.google.com/document')) {
        const docMatch = url.match(/\/d\/([a-zA-Z0-9_-]+)/);
        if (docMatch) {
            return `https://docs.google.com/document/d/${docMatch[1]}/export?format=pdf`;
        }
    }
    
    // Google Sheets → XLSX
    if (url.includes('docs.google.com/spreadsheets')) {
        const sheetMatch = url.match(/\/d\/([a-zA-Z0-9_-]+)/);
        if (sheetMatch) {
            return `https://docs.google.com/spreadsheets/d/${sheetMatch[1]}/export?format=xlsx`;
        }
    }
    
    // Google Slides → PDF
    if (url.includes('docs.google.com/presentation')) {
        const slideMatch = url.match(/\/d\/([a-zA-Z0-9_-]+)/);
        if (slideMatch) {
            return `https://docs.google.com/presentation/d/${slideMatch[1]}/export/pdf`;
        }
    }
    
    return url;  // Otros: devolver original
}
```

**Tabla de conversiones:**
| Tipo de URL | Patrón Original | Formato Descarga |
|-------------|-----------------|------------------|
| Google Drive file | `/file/d/{id}/view` | `/uc?export=download&id={id}` |
| Google Drive open | `/open?id={id}` | `/uc?export=download&id={id}` |
| Google Docs | `/document/d/{id}` | `/document/d/{id}/export?format=pdf` |
| Google Sheets | `/spreadsheets/d/{id}` | `/spreadsheets/d/{id}/export?format=xlsx` |
| Google Slides | `/presentation/d/{id}` | `/presentation/d/{id}/export/pdf` |

#### Botones de Acción

**Vista Lista:**
```html
<div class="resource-actions-group">
    <a href="${getDownloadUrl(res.url)}" download class="btn-download">
        ⬇️ Descargar
    </a>
    <a href="${res.url}" target="_blank" class="btn-open">
        🔗 Abrir
    </a>
</div>
```

**Vista Cards:**
```html
<div class="attachment-item">
    <a href="${att.url}" target="_blank" class="material-card__link">
        ${icon} ${displayTitle}
    </a>
    <a href="${downloadUrl}" download class="attachment-download">
        ⬇️
    </a>
</div>
```

---

### 4. Funciones Auxiliares

#### `renderAttachments(material)`
Renderiza todos los adjuntos de un material con botones de abrir y descargar.

#### `linkifyText(text)`
Convierte URLs en texto plano a links clickeables.

#### `truncateText(text, maxLength)`
Corta texto largo y agrega "...".

#### `formatDate(dateStr)`
Formatea fechas a formato español (ej: "20 dic 2025").

#### `getTypeIcon(type)` / `getTypeClass(type)`
Devuelve icono emoji y clase CSS según el tipo de material.

---

## Estilos CSS Clave

### Botones de Acción

```css
/* Botón Descargar (verde) */
.btn-download {
    background: var(--color-success, #34a853);
    color: white;
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
}

/* Botón Abrir (azul) */
.btn-open {
    background: var(--color-primary, #1a73e8);
    color: white;
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
}

/* Contenedor de acciones en tabla */
.resource-actions-group {
    display: flex;
    gap: 0.5rem;
    justify-content: flex-end;
}

/* Botón descarga en cards */
.attachment-download {
    width: 28px;
    height: 28px;
    background: var(--color-success, #34a853);
    border-radius: 4px;
}
```

---

## Flujo de Datos

```
Usuario carga /materials?id=COURSE_ID
         ↓
loadCourseInfo() → GET /api/courses/{id}
         ↓
loadMaterials() → GET /api/courses/{id}/materials?type=X&q=Y
         ↓
Render según currentView:
  - Cards: renderCardsView() → renderAttachments()
  - Lista: renderListView() (aplana attachments)
         ↓
Usuario hace click:
  - "Abrir" → target="_blank" (nueva pestaña)
  - "Descargar" → getDownloadUrl() + download attribute
```

---

## Historial de Versiones

| Versión | Fecha | Cambio |
|---------|-------|--------|
| v1.0.2 | 2025-12-16 | Soporte múltiples attachments por material |
| v1.0.3 | 2025-12-17 | URLs clickeables en descripciones (`linkifyText`) |
| v1.0.4 | 2025-12-17 | Sistema de filtros (tipo + búsqueda) |
| v1.0.5 | 2025-12-17 | Filtro para Notebooks |
| v1.0.8 | 2025-12-17 | Toggle vista Cards/Lista |
| v1.0.9 | 2025-12-20 | Descarga directa con `getDownloadUrl()` |
| v1.1.0 | 2025-12-20 | Selección múltiple, Descarga ZIP, Copiar a Drive |
| v1.1.1 | 2025-12-20 | Fix navegación Google Picker + extracción IDs |

---

## Análisis Dual

### Por qué SÍ:
- **UX completa**: El usuario puede abrir O descargar según necesite
- **Google-aware**: Convierte URLs de Drive/Docs a formato descarga
- **Dos vistas**: Cards para visual, Lista para eficiencia
- **Filtros frontend**: Complementan filtros backend

### Por qué NO (riesgos de hacerlo mal):
- **Solo "Abrir"**: Usuario no puede descargar fácilmente
- **Sin conversión URL**: Drive abriría visor en vez de descargar
- **Download en URL cruzada**: Algunos navegadores bloquean download de otros dominios
