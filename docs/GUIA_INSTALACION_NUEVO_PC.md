# 🚀 Guía de Instalación Paso a Paso para Nuevo Computador

Esta guía explica cómo instalar y configurar la aplicación "Gestor de Inventarios SIIGO" en un computador nuevo desde cero.

## 📋 Requisitos Previos

1.  **Acceso a Internet**.
2.  **Archivos del Proyecto**: Debes tener la carpeta completa del proyecto (la que contiene `main.py`, `gui.py`, `.env`, etc.).
3.  **Credenciales de SIIGO**: El archivo `.env` con las claves de acceso (ya incluido en la carpeta, pero es vital no perderlo).

---

## 🛠️ Paso 1: Instalar Python

El programa está hecho en Python, por lo que necesitamos instalarlo primero.

1.  Ve al sitio oficial de Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2.  Descarga la última versión (botón amarillo "Download Python 3.x.x").
3.  **¡IMPORTANTE!** Al ejecutar el instalador, asegúrate de marcar la casilla que dice:
    > **✅ Add python.exe to PATH**
    *(Si no marcas esto, el sistema no reconocerá los comandos de Python).*
4.  Haz clic en "Install Now" y espera a que termine.

---

## 📦 Paso 2: Preparar la Carpeta del Proyecto

1.  Copia la carpeta del proyecto (ej. `SIIGO API INVENTARIOS`) al nuevo computador. Puedes ponerla en `Documentos` o en el `Escritorio`.
2.  Abre la carpeta.
3.  Haz clic derecho en un espacio vacío dentro de la carpeta y selecciona **"Abrir en Terminal"** (o "Open in Terminal").
    *   *Si no ves esa opción:* Presiona la tecla `Shift` + `Clic Derecho` y selecciona "Abrir ventana de PowerShell aquí".

---

## 📚 Paso 3: Instalar Librerías Necesarias

En la ventana negra o azul que se abrió (la terminal), escribe el siguiente comando y presiona `Enter`:

```bash
pip install -r requirements.txt
```

Si por alguna razón ese comando falla o dice que no encuentra el archivo, puedes instalar las librerías manualmente escribiendo:

```bash
pip install requests python-dotenv ttkbootstrap
```

*Espera a que termine de descargar e instalar todo.*

---

## ⚙️ Paso 4: Verificar Configuración de API (.env)

El archivo `.env` es el corazón de la conexión con SIIGO.

1.  Busca el archivo llamado `.env` en la carpeta.
2.  Ábrelo con el "Bloc de notas".
3.  Asegúrate de que tenga las credenciales correctas. Debería verse algo así:

```env
COMPANY_1_NAME="Nombre Empresa 1"
COMPANY_1_USER="correo@empresa1.com"
COMPANY_1_KEY="clave_larga_y_rara_api_key..."

COMPANY_2_NAME="Nombre Empresa 2"
...
```

*Si copiaste la carpeta completa del computador anterior, este archivo ya debería estar listo y no necesitas tocar nada.*

---

## 🚀 Paso 5: Ejecutar la Aplicación

Tienes dos formas de abrir la aplicación:

### Opción A: Crear un Acceso Directo (Recomendado)
1.  Busca el archivo `Iniciar App.bat` en la carpeta.
2.  Haz clic derecho sobre él -> "Enviar a" -> "Escritorio (crear acceso directo)".
3.  Ahora puedes abrir el programa desde el escritorio con doble clic.

### Opción B: Ejecutar desde la Terminal
Si sigues en la ventana de terminal (paso 3), escribe:

```bash
python gui.py
```

---

## ❓ Solución de Problemas Comunes

**Error: "Python no se reconoce como un comando interno..."**
*   **Causa:** No marcaste la casilla "Add Python to PATH" al instalar.
*   **Solución:** Reinstala Python y asegúrate de marcar esa casilla.

**Error: "No module named 'requests'" o similar**
*   **Causa:** Faltó instalar las librerías.
*   **Solución:** Repite el Paso 3.

**La aplicación abre pero no carga datos**
*   **Causa:** Puede que no haya conexión a internet o las claves del archivo `.env` estén vencidas/incorrectas.
*   **Solución:** Verifica tu internet. Si persiste, verifica el archivo `.env`.

---
**¡Listo! La aplicación debería estar funcionando correctamente y conectándose a la API de SIIGO.**
