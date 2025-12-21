"""
Script de Diagnóstico - Classroom Explorer
==========================================

Este script ayuda a diagnosticar problemas comunes.

Ejecutar:
    python diagnostico.py
"""

print("=" * 60)
print("DIAGNÓSTICO - Classroom Explorer")
print("=" * 60)

# 1. Verificar que los cambios están en el código
print("\n1. ✅ Verificando cambios en el código...")

# Verificar fix v1.2.7 (detección de tipo en attachments)
try:
    with open('src/infrastructure/mappers/classroom_mapper.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'detected_type = self._detect_type_by_filename(title)' in content:
            print("   ✅ Fix v1.2.7 (detección por filename) PRESENTE")
        else:
            print("   ❌ Fix v1.2.7 NO encontrado")
        
        if 'detected_type = self._detect_type_by_url(url, title)' in content:
            print("   ✅ Fix v1.2.9 (detección por URL en links) PRESENTE")
        else:
            print("   ❌ Fix v1.2.9 NO encontrado")
except Exception as e:
    print(f"   ❌ Error leyendo mapper: {e}")

# Verificar fix v1.2.8 (prefijo de fecha)
try:
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'date_prefix' in content and "strftime('%Y-%m-%d_')" in content:
            print("   ✅ Fix v1.2.8 (prefijo de fecha) PRESENTE")
        else:
            print("   ❌ Fix v1.2.8 NO encontrado")
except Exception as e:
    print(f"   ❌ Error leyendo main.py: {e}")

try:
    with open('public/materials.html', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'data-date="${res.date}"' in content:
            print("   ✅ Fix v1.2.8 frontend (data-date) PRESENTE")
        else:
            print("   ❌ Fix v1.2.8 frontend NO encontrado")
except Exception as e:
    print(f"   ❌ Error leyendo materials.html: {e}")

# 2. Verificar variables de entorno
print("\n2. ✅ Verificando variables de entorno...")
import os
from dotenv import load_dotenv

load_dotenv()

critical_vars = {
    'GOOGLE_CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
    'GOOGLE_CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET'),
}

all_ok = True
for var_name, value in critical_vars.items():
    if not value or value.startswith('REEMPLAZA') or value.startswith('<'):
        print(f"   ❌ {var_name}: NO configurada o valor placeholder")
        all_ok = False
    else:
        print(f"   ✅ {var_name}: Configurada (longitud: {len(value)} chars)")

if all_ok:
    print("   ✅ Todas las variables críticas OK")

# 3. Verificar ultima modificación de archivos
print("\n3. ✅ Última modificación de archivos clave...")
import datetime

files_to_check = [
    'src/infrastructure/mappers/classroom_mapper.py',
    'main.py',
    'public/materials.html'
]

for filepath in files_to_check:
    try:
        import os
        mtime = os.path.getmtime(filepath)
        dt = datetime.datetime.fromtimestamp(mtime)
        print(f"   {filepath}: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"   ❌ {filepath}: Error - {e}")

print("\n" + "=" * 60)
print("INSTRUCCIONES:")
print("=" * 60)
print("""
Si los fixes están PRESENTES pero el problema persiste:

1. REINICIAR EL SERVIDOR (si estás en local):
   - Ctrl+C para detener el servidor
   - python main.py para reiniciarlo

2. LIMPIAR CACHÉ DEL NAVEGADOR:
   - Ctrl+F5 para recargar sin caché
   - O abrir en ventana de incógnito

3. VERIFICAR EN VERCEL (si estás en producción):
   - Ir a https://vercel.com/tu-proyecto
   - Verificar que el último deploy sea exitoso
   - Verificar que la fecha del deploy sea posterior a los commits

4. VERIFICAR LOS DATOS:
   - Los cambios solo afectan a NUEVAS cargas de datos
   - Prueba con un curso diferente
   - O recarga la página de materiales (F5)
""")
print("=" * 60)
