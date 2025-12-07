# Gestor de Inventarios Siigo - Aplicación Standalone

## 📦 Archivos Principales

### Ejecutable
- **GestorInventarioSiigo.exe** (33 MB) - Aplicación standalone completa
  - No requiere Python instalado
  - Incluye todas las dependencias
  - Con icono personalizado

### Accesos Directos
- **Iniciar App.bat** - Lanzador rápido del ejecutable
- **Iniciar Inventario.bat** - Lanzador del script Python (requiere Python)

## 🚀 Cómo Usar

### Opción 1: Ejecutable Standalone (Recomendado)
1. **Doble clic** en `GestorInventarioSiigo.exe`
2. O ejecuta `Iniciar App.bat`

**Ventajas:**
- ✅ No requiere Python instalado
- ✅ Más rápido de iniciar
- ✅ Portable - puedes copiar solo el .exe
- ✅ Icono personalizado en la barra de tareas

### Opción 2: Script Python
1. Ejecuta `Iniciar Inventario.bat`
2. O ejecuta `python gui.py` desde la terminal

**Requisitos:**
- Python 3.x instalado
- Dependencias instaladas (`pip install -r requirements.txt`)

## 📁 Estructura de Archivos

```
SIIGO API INVENTARIOS/
├── GestorInventarioSiigo.exe    ← Aplicación standalone
├── Iniciar App.bat               ← Lanzador del ejecutable
├── Iniciar Inventario.bat        ← Lanzador del script Python
├── app.ico                       ← Icono de la aplicación
├── gui.py                        ← Código fuente de la interfaz
├── main.py                       ← Script de actualización API
├── auth.py                       ← Autenticación Siigo
├── inventory.py                  ← Gestión de inventario
├── config.py                     ← Configuración
├── .env                          ← Credenciales (NO compartir)
└── requirements.txt              ← Dependencias Python
```

## 🔄 Actualización de Datos

Desde la aplicación:
1. Clic en **"🔄 Actualizar desde API"**
2. Espera a que se complete la descarga
3. Los datos se guardan en: `C:\Users\costo\OneDrive - Juan Pablo Muñoz Castaño\Inventario 2025\saldos\`

## ✨ Funcionalidades

### Filtros Disponibles
- 🔍 Búsqueda por código o nombre de producto
- 🏢 Filtro por empresa
- 📦 Filtro por bodegas (múltiple selección)
- 📊 Estado de stock (Positivos, Ceros, Negativos)
- 👁️ Mostrar/Ocultar productos ignorados
- 🏷️ Filtro por referencias de producto

### Ordenamiento
- 🔼🔽 Clic en cualquier encabezado de columna para ordenar
- Indicadores visuales (▲ ascendente, ▼ descendente)
- Ordenamiento inteligente (alfabético o numérico)

### Formato de Números
- Separador de miles con punto: `1.234.567,5`
- Aplicado en todas las cantidades

### Vistas
- 📋 **Detalle por Empresa** - Vista completa con todas las bodegas
- ∑ **Consolidado Global** - Suma total por producto

### Exportación
- 💾 Exportar a CSV (compatible con Excel)
- Formato con punto y coma (;) como separador

## 🛠️ Reconstruir el Ejecutable

Si modificas el código fuente:

```bash
python -m PyInstaller --onefile --windowed --icon=app.ico --name=GestorInventarioSiigo gui.py
Move-Item -Path "dist\GestorInventarioSiigo.exe" -Destination "." -Force
Remove-Item -Path "build" -Recurse -Force
Remove-Item -Path "dist" -Recurse -Force
Remove-Item -Path "*.spec" -Force
```

## 📝 Notas

- El ejecutable tiene ~33 MB porque incluye Python y todas las librerías
- Los datos se guardan en OneDrive para sincronización automática
- El archivo `.env` contiene las credenciales - **NO compartir**
- Los productos ignorados se guardan en `ignored_products.json`

## 🆘 Soporte

Si encuentras algún problema:
1. Verifica que el archivo `.env` existe y tiene las credenciales correctas
2. Asegúrate de tener conexión a internet para actualizar desde la API
3. Revisa que la carpeta de datos existe: `C:\Users\costo\OneDrive - Juan Pablo Muñoz Castaño\Inventario 2025\saldos\`

---

**Versión:** 1.0.0  
**Última actualización:** 24/11/2025
