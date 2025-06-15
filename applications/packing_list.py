def run():
    import streamlit as st
    import pandas as pd
    from openpyxl import load_workbook
    from copy import copy
    from io import BytesIO
    from PIL import Image

    # → Ton code V4 original commence ici

    # Configuration spécifique à cet outil
    # (NOTE : st.set_page_config a été déplacé dans app.py)
    #
    # Affichage du logo
    logo = Image.open("assets/logo_marketparts.png")
    st.image(logo, width=400)

    # Titre principal
    st.markdown(
        "<h1 style='color:#3a4e9f; font-size:24px;'>Générateur de Packing List</h1>",
        unsafe_allow_html=True
    )

    # Upload des fichiers F1 et F2
    col1, col2 = st.columns(2)
    with col1:
        uploaded_f1 = st.file_uploader("📁 1. Importer le fichier TO SHIP", type=["xlsx"], key="f1")
        with st.expander("📎 Voir le template (F1)"):
            st.image("assets/template_f1.png", caption="Exemple de fichier TO SHIP")
    with col2:
        uploaded_f2 = st.file_uploader("📁 2. Importer le fichier E LOG", type=["xlsx"], key="f2")
        with st.expander("📎 Voir le template (F2)"):
            st.image("assets/template_f2.png", caption="Exemple de fichier E LOG")

    # Traitement dès que les deux fichiers sont fournis
    if uploaded_f1 and uploaded_f2:
        # Lecture Excel
        df1 = pd.read_excel(uploaded_f1, engine="openpyxl")
        df2 = pd.read_excel(uploaded_f2, engine="openpyxl")

        # … ici toutes tes étapes de nettoyage, vlookup, formatage …
        # par exemple :
        # from modules.excel_formatter import format_excel_file
        # df_final = format_excel_file(df1, df2)

        # Mise en mémoire et téléchargement
        buffer = BytesIO()
        # df_final.to_excel(buffer, index=False)
        # buffer.seek(0)
        st.success("Fichier traité avec succès")
        st.download_button(
            "📥 Télécharger le fichier final",
            data=buffer,
            file_name="packing_list_output.xlsx"
        )

    # → Ton code V4 original se termine ici
