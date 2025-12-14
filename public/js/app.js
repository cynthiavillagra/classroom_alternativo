/**
 * Classroom Explorer - JavaScript
 * Python POO sin frameworks
 * 
 * POR QUÉ vanilla JS: Sin dependencias de frameworks
 */

// ═══════════════════════════════════════════════════════════════
// Paso 1: Verificar estado de autenticación al cargar
// ═══════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuthStatus();
    await checkApiStatus();
});

// ═══════════════════════════════════════════════════════════════
// Paso 2: Función para verificar autenticación
// ═══════════════════════════════════════════════════════════════
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/me');
        const data = await response.json();

        const loginBtn = document.getElementById('loginBtn');
        const userInfo = document.getElementById('userInfo');
        const userName = document.getElementById('userName');

        if (data.authenticated) {
            // Usuario autenticado
            if (loginBtn) loginBtn.style.display = 'none';
            if (userInfo) {
                userInfo.style.display = 'flex';
                userName.textContent = `Usuario: ${data.user_id}`;
            }
        } else {
            // Usuario no autenticado
            if (loginBtn) loginBtn.style.display = 'inline-flex';
            if (userInfo) userInfo.style.display = 'none';
        }
    } catch (error) {
        console.error('Error verificando auth:', error);
    }
}

// ═══════════════════════════════════════════════════════════════
// Paso 3: Verificar estado de APIs
// ═══════════════════════════════════════════════════════════════
async function checkApiStatus() {
    // Verificar Auth API
    await checkEndpoint('/api/auth/me', 'statusAuth');

    // Verificar si podemos acceder a courses (aunque dé 401)
    await checkEndpoint('/api/courses', 'statusCourses');
}

async function checkEndpoint(url, elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    try {
        const response = await fetch(url);

        // 200 o 401 significa que el endpoint funciona
        if (response.status === 200 || response.status === 401) {
            element.classList.add('success');
            element.classList.remove('error');
            element.querySelector('.status-icon').textContent = '✅';
        } else {
            element.classList.add('error');
            element.classList.remove('success');
            element.querySelector('.status-icon').textContent = '❌';
        }
    } catch (error) {
        element.classList.add('error');
        element.querySelector('.status-icon').textContent = '❌';
    }
}

// ═══════════════════════════════════════════════════════════════
// Paso 4: Utilidades
// ═══════════════════════════════════════════════════════════════
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Log para debugging
console.log('📚 Classroom Explorer cargado');
console.log('🤖 AI Stack: SDLC V5 + Google Antigravity + Claude Opus 4.5');
