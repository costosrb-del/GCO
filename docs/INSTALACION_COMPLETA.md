# INSTALACIÓN - Gestor de Inventarios Siigo
## Versión Completa con Actualización API

---

## 📦 CONTENIDO DEL PAQUETE

Has recibido los siguientes archivos:

```
SIIGO API INVENTARIOS/
├── GestorInventarioSiigo.exe    ← Aplicación principal
├── app.ico                       ← Icono
├── .env                          ← Credenciales API (CONFIDENCIAL)
├── main.py                       ← Script de actualización
├── auth.py                       ← Autenticación
├── inventory.py                  ← Gestión de inventario
├── config.py                     ← Configuración
├── Iniciar App.bat               ← Lanzador rápido
└── README.md                     ← Documentación
```

---

## 🚀 INSTALACIÓN PASO A PASO

### Paso 1: Copiar Archivos

1. **Crea una carpeta** en tu PC:
   - Recomendado: `C:\Inventarios\SIIGO\`
   - O en el Escritorio: `Escritorio\SIIGO API INVENTARIOS\`

2. **Copia TODOS los archivos** a esa carpeta
   - ⚠️ IMPORTANTE: Copia toda la carpeta completa
   - No copies solo el .exe

### Paso 2: Verificar Carpeta de Datos

La aplicación guarda los datos en:
```
C:\Users\TU_USUARIO\OneDrive - Juan Pablo Muñoz Castaño\Inventario 2025\saldos\
```

**Opciones:**

**A) Si tienes OneDrive configurado:**
- ✅ La carpeta se creará automáticamente
- ✅ Los datos se sincronizarán con otros usuarios

**B) Si NO tienes OneDrive:**
- Crea manualmente la carpeta:
  ```
  C:\Users\TU_USUARIO\OneDrive - Juan Pablo Muñoz Castaño\Inventario 2025\saldos\
  ```
- O modifica la ruta en el código (ver sección "Personalización")

### Paso 3: Ejecutar la Aplicación

1. **Doble clic** en `GestorInventarioSiigo.exe`
   - O ejecuta `Iniciar App.bat`

2. **Primera vez:**
   - Verás el Menú Principal
   - Clic en "📦 Inventario"
   - Si no hay datos, verás "Archivo de datos no encontrado"
   - ¡Esto es normal!

3. **Actualizar desde API:**
   - Clic en el botón **"🔄 Actualizar desde API"**
   - Espera 2-5 minutos (depende de la cantidad de productos)
   - Los datos se descargarán automáticamente

---

## ✅ FUNCIONALIDADES DISPONIBLES

### Con esta versión completa puedes:

- ✅ **Actualizar desde API de Siigo** (botón 🔄)
- ✅ Ver inventario de ambas empresas
- ✅ Filtrar por empresa, bodega, producto
- ✅ Ordenar columnas (clic en encabezados)
- ✅ Exportar a Excel/CSV
- ✅ Ocultar/mostrar productos
- ✅ Ver vista consolidada
- ✅ Ver total de unidades

---

## 🔒 SEGURIDAD - IMPORTANTE

### ⚠️ Archivo .env (CONFIDENCIAL)

El archivo `.env` contiene las credenciales de acceso a la API de Siigo:

```
COMPANY_1_NAME=Armonia Cosmetica S.A.S.
COMPANY_1_USER=tu_usuario
COMPANY_1_KEY=tu_clave_secreta
...
```

**NUNCA:**
- ❌ Compartas este archivo públicamente
- ❌ Lo subas a internet o redes sociales
- ❌ Lo envíes por correo sin cifrar

**SIEMPRE:**
- ✅ Guárdalo en un lugar seguro
- ✅ Haz backup del archivo
- ✅ Compártelo solo con personas autorizadas

---

## 🔧 PERSONALIZACIÓN (Opcional)

### Cambiar Ruta de Datos

Si quieres guardar los datos en otra ubicación:

1. Abre `gui.py` con un editor de texto
2. Busca la línea (línea 15):
   ```python
   DATA_DIR = r"C:\Users\costo\OneDrive - Juan Pablo Muñoz Castaño\Inventario 2025\saldos"
   ```
3. Cámbiala por tu ruta preferida:
   ```python
   DATA_DIR = r"C:\MiCarpeta\Inventarios"
   ```
4. Guarda el archivo
5. Reconstruye el ejecutable (ver README.md)

### Agregar Más Empresas

Si necesitas agregar más empresas al sistema:

1. Abre el archivo `.env`
2. Agrega las nuevas credenciales:
   ```
   COMPANY_3_NAME=Nombre Empresa 3
   COMPANY_3_USER=usuario3
   COMPANY_3_KEY=clave3
   ```
3. Guarda y reinicia la aplicación

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### "Archivo de datos no encontrado"
**Solución:**
1. Clic en "🔄 Actualizar desde API"
2. Espera a que descargue los datos
3. Si el error persiste, verifica:
   - Conexión a internet
   - Credenciales en `.env`
   - Carpeta de datos existe

### "Error de autenticación" o "Error al actualizar"
**Solución:**
1. Verifica el archivo `.env`:
   - Usuario y clave correctos
   - Sin espacios extras
   - Formato correcto
2. Verifica conexión a internet
3. Contacta al administrador si persiste

### "Windows protegió tu PC"
**Solución:**
1. Clic en "Más información"
2. Clic en "Ejecutar de todas formas"
3. Es normal para ejecutables no firmados digitalmente

### La aplicación se cierra inmediatamente
**Solución:**
1. Verifica que copiaste TODOS los archivos
2. Ejecuta como Administrador:
   - Clic derecho en el .exe
   - "Ejecutar como administrador"
3. Verifica que tienes Windows 10/11 de 64 bits

### Los datos no se sincronizan con OneDrive
**Solución:**
1. Verifica que OneDrive está instalado y activo
2. Verifica que la carpeta está dentro de OneDrive
3. Espera unos minutos para la sincronización
4. O usa una ruta local (ver "Personalización")

---

## 📊 FLUJO DE TRABAJO RECOMENDADO

### Primera Vez:
1. Instalar archivos en carpeta
2. Ejecutar aplicación
3. Actualizar desde API (botón 🔄)
4. Esperar descarga completa
5. ¡Listo para usar!

### Uso Diario:
1. Abrir aplicación
2. Usar filtros y consultas
3. Exportar si necesitas
4. Cerrar aplicación

### Actualización Periódica:
- Clic en "🔄 Actualizar desde API"
- Recomendado: 1 vez al día o según necesidad
- Los datos se guardan automáticamente

---

## 📞 SOPORTE

Si tienes problemas:

1. **Lee esta guía completa**
2. **Revisa el archivo README.md**
3. **Contacta al administrador del sistema**

---

## 📝 NOTAS IMPORTANTES

- El ejecutable tiene ~33 MB (incluye Python y librerías)
- La primera actualización puede tardar más tiempo
- Los datos se guardan localmente y en OneDrive (si está configurado)
- Puedes usar la aplicación sin internet (solo para consultar datos ya descargados)
- Para actualizar desde API SÍ necesitas internet

---

**Versión:** 1.0.0  
**Fecha:** 24/11/2025  
**Desarrollado para:** Origen Botánico

---

## ✅ CHECKLIST DE INSTALACIÓN

- [ ] Copié todos los archivos a una carpeta
- [ ] Verifiqué que el archivo .env está presente
- [ ] Ejecuté GestorInventarioSiigo.exe
- [ ] Actualicé desde la API exitosamente
- [ ] Puedo ver los datos de inventario
- [ ] Probé los filtros y ordenamiento
- [ ] Guardé esta guía para futuras referencias

¡Listo! Ya puedes usar el Gestor de Inventarios Siigo 🎉
