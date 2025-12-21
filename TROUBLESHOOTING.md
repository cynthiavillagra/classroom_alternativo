# 🔧 TROUBLESHOOTING - Cambios No Se Aplican

## ⚠️ PROBLEMA
Los cambios están en el código pero NO se ven en la aplicación.

## ✅ DIAGNÓSTICO REALIZADO
Ejecuté `diagnostico.py` y confirmé que:
- ✅ Todos los fixes están en el código
- ✅ Variables de entorno configuradas
- ✅ Commits pusheados correctamente

## 🎯 CAUSA RAÍZ
**Los cambios en Python NO se aplican automáticamente.**

Necesitas:
1. **LOCAL**: Reiniciar el servidor Python
2. **VERCEL**: Redesplegar la aplicación

---

## 📋 SOLUCIÓN RÁPIDA

### Si estás en LOCAL (desarrollo):
```bash
# 1. Detener servidor (Ctrl+C)
# 2. Reiniciar
python main.py

# 3. En el navegador: Ctrl+F5 (recarga sin caché)
```

### Si estás en VERCEL (producción):
```bash
# Opción 1: Deploy manual
vercel --prod

# Opción 2: Desde dashboard de Vercel
# - Ve a https://vercel.com/
# - Busca tu proyecto
# - Haz clic en "Redeploy"
```

---

## 🧪 CÓMO VERIFICAR QUE FUNCIONA

### 1. Filtro "Documentos"
- Ve a cualquier curso con materiales
- Haz clic en el filtro "📝 Documentos"
- Deberías ver:
  - ✅ Google Slides
  - ✅ Google Docs
  - ✅ Google Sheets
  - ✅ Archivos .ppt, .docx, .md

### 2. Prefijo de Fecha
- Selecciona algunos archivos
- Haz clic en "📦 Descargar ZIP" o "📁 Copiar a Drive"
- Los archivos deberían tener formato:
  ```
  2024-12-15_nombre_archivo.pdf
  2024-11-20_presentacion.pptx
  ```

---

## ❓ SI SIGUE SIN FUNCIONAR

1. **Verifica que el servidor esté actualizado:**
   ```bash
   python diagnostico.py
   ```

2. **Limpia TODA la caché del navegador:**
   - Chrome: Configuración → Privacidad → Borrar datos de navegación
   - O usa ventana de incógnito

3. **Verifica en Vercel (si aplica):**
   - Dashboard → Deployments
   - Último deploy debe ser posterior a: **2025-12-21 18:20**
   - Estado debe ser: **✅ Ready**

4. **Prueba con datos frescos:**
   - Abre un curso diferente
   - Recarga la página completamente (F5)
   - Los datos viejos pueden estar cacheados

---

## 📞 CONTACTO DE SOPORTE
Si después de seguir estos pasos el problema persiste:
- Envía captura del output de `python diagnostico.py`
- Indica si estás en LOCAL o VERCEL
- Envía URL del curso que estás probando
