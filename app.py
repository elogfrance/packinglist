import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from copy import copy
from io import BytesIO
from PIL import Image

def run():
    # Bouton retour à l’accueil
    if st.button("⬅️ Retour à l’accueil"):
        st.experimental_set_query_params(page="home")
        st.rerun()

    # Affichage du logo
    logo = Image.open("logo_marketparts.png")
    st.image(logo, width=400)

    # Titre principal
    st.markdown(
        "<h1 style='color:#3a4e9f; font-size:24px;'>Générateur de Packing List</h1>",
        unsafe_allow_html=True
    )

    # Upload des fichiers
    col1, col2 = st.columns(2)

    with col1:
        uploaded_f1 = st.file_uploader("📁 1. Importer le fichier TO SHIP", type=["xlsx"], key="f1")
        with st.expa
