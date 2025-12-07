import sys
import os

# Agregamos la carpeta 'src' al path del sistema para que Python encuentre los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importamos la aplicación principal directamente
# Al estar 'src' en el path, los imports internos de la app (como 'import utils') funcionarán correctamente
import streamlit_app
