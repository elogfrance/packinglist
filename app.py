
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
logo = Image.open("logo v3.png")
st.image(logo, width=200)

# Titre principal
st.markdown("<h1 style='color:#3a4e9f;'>📦 Générateur de Packing List</h1>", unsafe_allow_html=True)
st.markdown("### 📁 Étape 1 : Importer vos fichiers Excel")

# Import F1 et F2 en colonnes séparées
col1, col2 = st.columns(2)

with col1:
    uploaded_f1 = st.file_uploader("📁 1. Importer le fichier **F1** (principal)", type=["xlsx"], key="f1")

with col2:
    uploaded_f2 = st.file_uploader("📁 2. Importer le fichier **F2** (références Vlookup)", type=["xlsx"], key="f2")

# Traitement à l'appui du bouton
if uploaded_f1 and uploaded_f2:
    try:
        # Chargement des fichiers
        wb_f1 = load_workbook(uploaded_f1)
        ws_f1 = wb_f1.active
        wb_f2 = load_workbook(uploaded_f2, data_only=True)
        ws_f2 = wb_f2.active

        # Suppression des colonnes "Unit Price" et "Total Price"
        headers = [cell.value for cell in ws_f1[11]]
        for idx in sorted([i for i, h in enumerate(headers) if h in ["Unit Price", "Total Price"]], reverse=True):
            ws_f1.delete_cols(idx + 1)

        # Fusion de la cellule "Delivery Note / Bon de livraison" de A à H
        for row in ws_f1.iter_rows(min_row=1, max_row=20, max_col=8):
            for cell in row:
                if cell.value == "Delivery Note / Bon de livraison":
                    try:
                        ws_f1.unmerge_cells(start_row=cell.row, start_column=1, end_row=cell.row, end_column=9)
                    except:
                        pass
                    ws_f1.merge_cells(start_row=cell.row, start_column=1, end_row=cell.row, end_column=8)
                    break

        # Nettoyage sécurisé H9/I9
        h9 = ws_f1["H9"].value or ""
        try:
            i9 = ws_f1["I9"].value or ""
        except:
            i9 = ""
        ws_f1["H9"].value = f"{h9} {i9}".strip()

        try:
            ws_f1["I9"].value = None
        except:
            pass

        try:
            ws_f1.merge_cells("H9:I9")
        except:
            pass

        # Ajout du champ "N° de palette" en H11 avec le style de G11
        ws_f1["H11"].value = "N° de palette"
        if ws_f1["G11"].has_style:
            for attr in ["font", "border", "fill", "number_format", "protection", "alignment"]:
                setattr(ws_f1["H11"], attr, copy(getattr(ws_f1["G11"], attr)))

        # Recherche V depuis F2 vers F1
        for row in range(12, ws_f1.max_row + 1):
            key = ws_f1[f"A{row}"].value
            if not key:
                continue
            for r in ws_f2.iter_rows(min_row=1, max_col=5):
                if r[3].value == key:
                    ws_f1[f"H{row}"].value = r[4].value
                    break

        # Sauvegarde dans la mémoire
        output = BytesIO()
        wb_f1.save(output)
        output.seek(0)

     
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger packing list excel",
            data=output.getvalue(),
            file_name="PackingList.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Une erreur est survenue : {e}")
