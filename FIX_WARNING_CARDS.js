// [FIX v1.3.2] Agregar esto dentro de la función applyCurrentView, después de obtener bulkActionsBar

const cardViewWarning = document.getElementById('cardViewWarning');

// [FIX v1.3.2] Mostrar/ocultar warning y barra según vista
if (currentView === 'cards') {
    // Vista Cards: Mostrar warning, ocultar barra de acciones
    cardViewWarning.style.display = materials && materials.length > 0 ? 'block' : 'none';
    bulkActionsBar.style.display = 'none';
} else {
    // Vista Lista: Ocultar warning, mostrar barra si hay materiales
    cardViewWarning.style.display = 'none';
    bulkActionsBar.style.display = materials && materials.length > 0 ? 'flex' : 'none';
}

// REEMPLAZAR las líneas 816-821 con el código de arriba
