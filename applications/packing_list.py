# applications/packing_list.py

def run():
    import streamlit as st
    import pandas as pd
    from openpyxl import load_workbook
    from copy import copy
    from io import BytesIO
    import os
    from PIL import Image

    # Chemin absolu vers le dossier racine du projet
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    # Charger le logo depuis assets/
    logo_path = os.path.join(BASE_DIR, "assets", "logo_marketparts.png")
    logo = Image.open(logo_path)
    st.image(logo, width=400)

    # Titre principal
    st.markdown(
        "<h1 style='color:#3a4e9f; font-size:24px;'>Générateur de Packing List</h1>",
        unsafe_allow_html=True
    )

    # Import des fichiers F1 et F2
    col1, col2 = st.columns(2)
    with col1:
        uploaded_f1 = st.file_uploader("📁 1. Importer le fichier TO SHIP", type=["xlsx"], key="f1")
        with st.expander("📎 Voir le template (F1)"):
            template1 = os.path.join(BASE_DIR, "assets", "template_f1.png")
            st.image(template1, caption="Exemple de fichier TO SHIP")
    with col2:
        uploaded_f2 = st.file_uploader("📁 2. Importer le fichier E LOG", type=["xlsx"], key="f2")
        with st.expander("📎 Voir le template (F2)"):
            template2 = os.path.join(BASE_DIR, "assets", "template_f2.png")
            st.image(template2, caption="Exemple de fichier E LOG")

    # Traitement automatique dès que les deux fichiers sont fournis
    if uploaded_f1 and uploaded_f2:
        # Lecture des données Excel
        df1 = pd.read_excel(uploaded_f1, engine="openpyxl")
        df2 = pd.read_excel(uploaded_f2, engine="openpyxl")

        # --- Ici, place ta logique de nettoyage, vlookup et mise en forme ---
        # Exemples :
        # from modules.excel_formatter import format_excel_file
        # df_final = format_excel_file(df1, df2)
        #
        # OU si tu as un module vlookup_logic :
        # from modules.vlookup_logic import apply_vlookup
        # df1_with_vlookup = apply_vlookup(df1, df2)

        # Pour l’exemple, on réutilise df1 comme df_final
        df_final = df1.copy()

        # Préparer le buffer pour téléchargement
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_final.to_excel(writer, index=False, sheet_name="PackingList")
            writer.save()
        buffer.seek(0)

        st.success("Fichier traité avec succès")
        st.download_button(
            "📥 Télécharger le fichier final",
            data=buffer,
            file_name="packing_list_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
