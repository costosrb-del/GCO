import sys
import os

# 1. Agregamos la carpeta 'src' al sistema para que encuentre los módulos (auth, utils, etc)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.append(src_dir)

# 2. Definimos la ruta del script real
script_path = os.path.join(src_dir, 'streamlit_app.py')

# 3. Ejecutamos el código del script principal manualmente
# Esto evita problemas de "caching" de imports que dejan la pantalla en blanco al recargar
if os.path.exists(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code, globals())
else:
    import streamlit as st
    st.error(f"No se encontró el archivo principal en: {script_path}")
