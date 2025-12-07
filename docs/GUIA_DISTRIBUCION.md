# Guía de Distribución - Gestor de Inventarios Siigo

## 🎯 Dos Formas de Compartir el Programa

### Opción 1: Solo Consulta (Recomendado para usuarios finales)

**Qué compartir:**
```
📁 Carpeta a compartir/
├── GestorInventarioSiigo.exe
├── app.ico (opcional)
└── INSTRUCCIONES_INSTALACION.md
```

**Ventajas:**
- ✅ Muy simple y seguro
- ✅ No expones credenciales de Siigo
- ✅ Usuario solo puede consultar y filtrar

**Limitaciones:**
- ❌ No puede actualizar desde API
- ⚠️ Debes compartirles el archivo de datos actualizado periódicamente

**Cómo compartir datos:**
1. Actualiza desde la API en tu PC
2. Comparte el archivo: `C:\Users\costo\OneDrive - Juan Pablo Muñoz Castaño\Inventario 2025\saldos\consolidated_inventory.json`
3. Ellos lo copian en su carpeta de datos

---

### Opción 2: Instalación Completa (Para administradores)

**Qué compartir:**
```
📁 SIIGO API INVENTARIOS/ (carpeta completa)
├── GestorInventarioSiigo.exe
├── app.ico
├── .env                    ⚠️ CREDENCIALES
├── main.py
├── auth.py
├── inventory.py
├── config.py
├── Iniciar App.bat
└── README.md
```

**Ventajas:**
- ✅ Puede actualizar desde API de Siigo
- ✅ Totalmente autónomo

**⚠️ IMPORTANTE - Seguridad:**
- El archivo `.env` tiene las credenciales de acceso a Siigo
- Solo compártelo con personas autorizadas
- Considera crear credenciales separadas por usuario en Siigo

---

## 📋 Pasos para Compartir

### Para Opción 1 (Solo Consulta):

1. **Crear carpeta para compartir:**
   ```
   Nueva carpeta/
   ├── GestorInventarioSiigo.exe
   ├── app.ico
   └── INSTRUCCIONES_INSTALACION.md
   ```

2. **Comprimir en ZIP:**
   - Clic derecho → "Enviar a" → "Carpeta comprimida"
   - Nombre sugerido: `GestorInventarioSiigo_v1.0.zip`

3. **Compartir:**
   - Por correo, USB, OneDrive, etc.

4. **Compartir datos (periódicamente):**
   - Archivo: `consolidated_inventory.json`
   - Ubicación en tu PC: `C:\Users\costo\OneDrive - Juan Pablo Muñoz Castaño\Inventario 2025\saldos\`

### Para Opción 2 (Completa):

1. **Copiar carpeta completa:**
   ```
   SIIGO API INVENTARIOS/
   ```

2. **⚠️ ANTES de compartir el .env:**
   - Considera si el usuario realmente necesita actualizar desde API
   - Evalúa crear credenciales separadas en Siigo
   - O elimina el .env y comparte solo datos actualizados

3. **Comprimir y compartir**

---

## 🔒 Recomendaciones de Seguridad

### Si compartes credenciales (.env):

1. **Crear usuario específico en Siigo:**
   - Con permisos solo de lectura
   - Solo para inventarios
   - Diferente al usuario principal

2. **Documentar quién tiene acceso:**
   - Llevar registro de a quién se compartió
   - Fecha de compartición
   - Propósito

3. **Cambiar credenciales periódicamente:**
   - Cada 3-6 meses
   - Si alguien deja de necesitar acceso

### Alternativa más segura:

**Centralizar actualización:**
- Solo TÚ actualizas desde la API
- Compartes el archivo `consolidated_inventory.json` actualizado
- Ellos solo consultan con el ejecutable
- Puedes usar OneDrive compartido para sincronización automática

---

## 📊 Sincronización Automática con OneDrive

**Mejor opción para múltiples usuarios:**

1. **Compartir carpeta de OneDrive:**
   ```
   OneDrive/Inventario 2025/saldos/
   ```

2. **Configurar en cada PC:**
   - Instalar OneDrive
   - Sincronizar la carpeta compartida
   - El ejecutable leerá automáticamente los datos actualizados

3. **Ventajas:**
   - ✅ Datos siempre actualizados
   - ✅ No necesitas enviar archivos manualmente
   - ✅ Todos ven los mismos datos
   - ✅ No expones credenciales de API

---

## 🎁 Paquete Recomendado para Compartir

```
GestorInventarioSiigo_v1.0.zip
├── GestorInventarioSiigo.exe
├── app.ico
├── INSTRUCCIONES_INSTALACION.md
└── LEEME.txt (instrucciones rápidas)
```

**Contenido de LEEME.txt:**
```
GESTOR DE INVENTARIOS SIIGO
===========================

1. Descomprime esta carpeta
2. Doble clic en GestorInventarioSiigo.exe
3. Lee INSTRUCCIONES_INSTALACION.md para más detalles

Para obtener datos actualizados, contacta al administrador.

Versión: 1.0.0
```

---

## ✅ Checklist antes de Compartir

- [ ] Decidir: ¿Solo consulta o acceso completo?
- [ ] Si solo consulta: Incluir solo .exe + icono + instrucciones
- [ ] Si completo: Evaluar seguridad de compartir .env
- [ ] Crear INSTRUCCIONES_INSTALACION.md
- [ ] Comprimir en ZIP
- [ ] Probar en otro PC (si es posible)
- [ ] Documentar a quién se compartió

---

**Última actualización:** 24/11/2025  
**Versión del programa:** 1.0.0
