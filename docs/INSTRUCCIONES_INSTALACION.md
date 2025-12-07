# Instrucciones para Instalar - Gestor de Inventarios Siigo

## 📦 Instalación Simple (Solo Consulta)

### Archivos Recibidos:
- `GestorInventarioSiigo.exe` (33 MB)
- `app.ico` (opcional)

### Pasos de Instalación:

1. **Crear una carpeta** en tu PC:
   - Ejemplo: `C:\Inventarios\` o en el Escritorio

2. **Copiar los archivos** a esa carpeta

3. **Ejecutar la aplicación**:
   - Doble clic en `GestorInventarioSiigo.exe`

4. **Primera vez**:
   - La aplicación mostrará "Archivo de datos no encontrado"
   - Esto es normal - necesitas que te compartan los datos

### 📊 Obtener Datos de Inventario:

**Opción A: Archivo compartido**
- Pide el archivo `consolidated_inventory.json`
- Créalo en: `C:\Users\TU_USUARIO\OneDrive - Juan Pablo Muñoz Castaño\Inventario 2025\saldos\`
- O ajusta la ruta en el código

**Opción B: Carpeta compartida**
- Si tienes acceso a OneDrive compartido, los datos se sincronizarán automáticamente

### ✅ Funcionalidades Disponibles:

- ✅ Ver inventario completo
- ✅ Filtrar por empresa, bodega, producto
- ✅ Ordenar columnas (clic en encabezados)
- ✅ Exportar a Excel/CSV
- ✅ Ocultar/mostrar productos
- ❌ NO puede actualizar desde API Siigo (requiere credenciales)

### 🔄 Actualizar Datos:

Para tener datos actualizados:
1. Pide a quien tiene acceso a la API que actualice
2. Te comparte el nuevo archivo `consolidated_inventory.json`
3. Reemplazas el archivo en tu carpeta
4. Reinicias la aplicación

---

## 🆘 Problemas Comunes:

**"Archivo de datos no encontrado"**
- Solución: Necesitas el archivo `consolidated_inventory.json` en la ruta correcta

**"Windows protegió tu PC"**
- Solución: Clic en "Más información" → "Ejecutar de todas formas"
- Es normal para ejecutables no firmados

**La aplicación no inicia**
- Verifica que tienes Windows 10/11 de 64 bits
- Intenta ejecutar como Administrador (clic derecho → "Ejecutar como administrador")

---

**Versión:** 1.0.0  
**Soporte:** Contacta al administrador del sistema
