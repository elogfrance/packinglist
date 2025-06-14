import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from copy import copy
from io import BytesIO
from PIL import Image

# CONFIG PAGE
st.set_page_config(page_title="Générateur de Packing List", layout="wide")

# SIDEBAR - RÉGLAGES
st.sidebar.title("⚙️ Réglages d'affichage")
logo_width = st.sidebar.slider("Taille du logo", 50, 500, 200)
title_size = st.sidebar.slider("Taille du titre", 10, 80, 40)
button_size = st.sidebar.slider("Taille du bouton", 10, 30, 16)
font_size = st.sidebar.slider("Taille du texte général", 10, 24, 14)

# STYLE GLOBAL
st.markdown(
    f"""<style>
    body, .stApp {{
        font-size: {font_size}px;
    }}
    .stButton>button {{
        font-size: {button_size}px !important;
    }}
    </style>""",
    unsafe_allow_html=True
)

# LOGO
logo = Image.open("logo v3.png")
st.image(logo, width=logo_width)

# TITRE
st.markdown(
    f"<h1 style='color:#3a4e9f; font-size:{title_size}px;'>📦 Générateur de Packing List</h1>",
    unsafe_allow_html=True
)

st.markdown("### 📁 Étape 1 : Importer vos fichiers Excel")
col1, col2 = st.columns(2)
with col1:
    uploaded_f1 = st.file_uploader("📄 Fichier **F1** (principal)", type=["xlsx"], key="f1")
with col2:
    uploaded_f2 = st.file_uploader("📄 Fichier **F2** (références Vlookup)", type=["xlsx"], key="f2")

# TRAITEMENT
if uploaded_f1 and uploaded_f2:
    try:
        wb_f1 = load_workbook(uploaded_f1)
        ws_f1 = wb_f1.active
        wb_f2 = load_workbook(uploaded_f2, data_only=True)
        ws_f2 = wb_f2.active

        # Supprimer colonnes
        headers = [cell.value for cell in ws_f1[11]]
        for idx in sorted([i for i, h in enumerate(headers) if h in ["Unit Price", "Total Price"]], reverse=True):
            ws_f1.delete_cols(idx + 1)

        # Fusion titre A à H
        for row in ws_f1.iter_rows(min_row=1, max_row=20, max_col=8):
            for cell in row:
                if cell.value == "Delivery Note / Bon de livraison":
                    try:
                        ws_f1.unmerge_cells(start_row=cell.row, start_column=1, end_row=cell.row, end_column=9)
                    except:
                        pass
                    ws_f1.merge_cells(start_row=cell.row, start_column=1, end_row=cell.row, end_column=8)
                    break

        # Fusion H9/I9
        h9 = ws_f1["H9"].value or ""
        try:
            i9 = ws_f1["I9"].value or ""
        except:
            i9 = ""
        ws_f1["H9"].value = f"{h9} {i9}".strip()
        try:
            ws_f1["I9"].value = None
            ws_f1.merge_cells("H9:I9")
        except:
            pass

        # "N° de palette"
        ws_f1["H11"].value = "N° de palette"
        if ws_f1["G11"].has_style:
            for attr in ["font", "border", "fill", "number_format", "protection", "alignment"]:
                setattr(ws_f1["H11"], attr, copy(getattr(ws_f1["G11"], attr)))

        # Recherche V
        for row in range(12, ws_f1.max_row + 1):
            key = ws_f1[f"A{row}"].value
            if not key:
                continue
            for r in ws_f2.iter_rows(min_row=1, max_col=5):
                if r[3].value == key:
                    ws_f1[f"H{row}"].value = r[4].value
                    break

        output = BytesIO()
        wb_f1.save(output)
        output.seek(0)

        df_result = pd.read_excel(output)
        st.subheader("📊 Aperçu du fichier final")
        st.dataframe(df_result)

        st.download_button(
            label="📥 Télécharger le fichier final (Excel)",
            data=output.getvalue(),
            file_name="PackingList_v3.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Erreur : {e}")
