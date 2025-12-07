# Script para crear paquete de distribución
# Ejecutar: python crear_paquete.py

import os
import shutil
from datetime import datetime

# Archivos necesarios para distribución completa (con API)
archivos_distribucion = [
    "GestorInventarioSiigo.exe",
    "app.ico",
    ".env",
    "main.py",
    "auth.py",
    "inventory.py",
    "config.py",
    "Iniciar App.bat",
    "README.md",
    "INSTALACION_COMPLETA.md",
    "LEEME.txt",
    "requirements.txt"
]

# Crear carpeta de distribución
fecha = datetime.now().strftime("%Y%m%d")
carpeta_dist = f"GestorInventarioSiigo_Completo_{fecha}"

print(f"Creando paquete de distribucion: {carpeta_dist}")

# Crear carpeta si no existe
if os.path.exists(carpeta_dist):
    shutil.rmtree(carpeta_dist)
os.makedirs(carpeta_dist)

# Copiar archivos
archivos_copiados = 0
archivos_faltantes = []

for archivo in archivos_distribucion:
    if os.path.exists(archivo):
        shutil.copy2(archivo, carpeta_dist)
        print(f"[OK] Copiado: {archivo}")
        archivos_copiados += 1
    else:
        print(f"[X] No encontrado: {archivo}")
        archivos_faltantes.append(archivo)

print(f"\n{'='*50}")
print(f"Archivos copiados: {archivos_copiados}/{len(archivos_distribucion)}")

if archivos_faltantes:
    print(f"\n[!] Archivos faltantes:")
    for archivo in archivos_faltantes:
        print(f"  - {archivo}")

# Crear archivo ZIP
print(f"\nCreando archivo ZIP...")
nombre_zip = f"{carpeta_dist}.zip"

try:
    shutil.make_archive(carpeta_dist, 'zip', carpeta_dist)
    print(f"[OK] ZIP creado: {nombre_zip}")
    
    # Obtener tamaño del ZIP
    tamano_mb = os.path.getsize(nombre_zip) / (1024 * 1024)
    print(f"  Tamaño: {tamano_mb:.2f} MB")
except Exception as e:
    print(f"[X] Error al crear ZIP: {e}")

print(f"\n{'='*50}")
print(f"[LISTO] Paquete listo para compartir:")
print(f"   Carpeta: {carpeta_dist}/")
print(f"   ZIP: {nombre_zip}")
print(f"\n[INFO] Puedes compartir el archivo ZIP por:")
print(f"   - Correo electronico")
print(f"   - OneDrive / Google Drive")
print(f"   - USB")
print(f"   - Red local")
print(f"\n[IMPORTANTE] El archivo .env contiene credenciales")
print(f"   Solo compartelo con personas autorizadas")
print(f"\n{'='*50}")
