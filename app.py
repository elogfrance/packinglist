import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from copy import copy
from io import BytesIO
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Packing List",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Affichage du logo
logo = Image.open("logo_marketparts.png")
st.image(logo, width=400)

# Titre principal
st.markdown(
    "<h1 style='color:#3a4e9f; font-size:24px;'>Générateur de Packing List</h1>",
    unsafe_allow_html=True
)

# Import F1 et F2 en colonnes séparées
col1, col2 = st.columns(2)

wit
