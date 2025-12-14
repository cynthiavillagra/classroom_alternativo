# 📄 vercel.json — Manual Técnico

**Archivo:** `vercel.json`  
**Propósito:** Configuración para deploy en Vercel Serverless  
**Trazabilidad:** RNF-DEPL01 (Deployment), Infraestructura

---

## 📐 Estrategia de Construcción Incremental

1. **Paso 1 — version:** Versión del schema de Vercel (2)
2. **Paso 2 — builds:** Define cómo construir el proyecto
3. **Paso 3 — routes:** Mapea URLs a funciones serverless
4. **Paso 4 — env:** Variables de entorno (opcional)

---

## 📝 Contenido Actual

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    }
  ]
}
```

---

## 🎓 Aclaración Metodológica

Este archivo es JSON de configuración. No tiene prueba atómica con Python, pero se puede validar sintácticamente.

---

## 🔥 Prueba de Fuego

### Verificación de sintaxis JSON
```powershell
python -c "import json; json.load(open('vercel.json')); print('✅ vercel.json válido')"
```

### Salida Esperada
```
✅ vercel.json válido
```

---

## 🔍 Análisis Dual

### ✅ POR QUÉ SÍ Vercel Serverless

| Beneficio | Explicación |
|-----------|-------------|
| **Gratis** | Tier gratuito generoso |
| **Sin servidor** | No hay que gestionar infraestructura |
| **Auto-scaling** | Escala automáticamente |
| **Deploy fácil** | Push a GitHub = deploy automático |

### ❌ POR QUÉ NO Docker/VPS (por ahora)

| Razón | Detalle |
|-------|---------|
| **Overkill** | Más complejo para MVP |
| **Costo** | VPS tiene costo mensual fijo |
| **Mantenimiento** | Hay que gestionar servidor |
