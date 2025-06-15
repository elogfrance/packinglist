import streamlit as st
from io import BytesIO
from PIL import Image

from data_processing import (
    load_excel_files,
    clean_and_merge_columns,
    copy_cell_style,
    fill_palette_number,
    save_workbook_to_bytes,
)


def main():
    # Configuration de la page
    st.set_page_config(
        page_title="Générateur de Packing List",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Affichage du logo
    logo = Image.open("logo_marketparts.png")
    st.image(logo, width=400)

    # Titre principal
    st.markdown(
        "<h1 style='color:#3a4e9f; font-size:24px;'>Générateur de Packing List</h1>",
        unsafe_allow_html=True,
    )

    # Import F1 et F2 en colonnes séparées
    col1, col2 = st.columns(2)

    with col1:
        uploaded_f1 = st.file_uploader(
            "📁 1. Importer le fichier TO SHIP", type=["xlsx"], key="f1"
        )
        with st.expander("📎 Voir le template (F1)"):
            st.image("template_f1.png", caption="Exemple de fichier TO SHIP")

    with col2:
        uploaded_f2 = st.file_uploader(
            "📁 2. Importer le fichier E LOG", type=["xlsx"], key="f2"
        )
        with st.expander("📎 Voir le template (F2)"):
            st.image("template_f2.png", caption="Exemple de fichier E LOG")

    if uploaded_f1 and uploaded_f2:
        try:
            wb_f1, ws_f1, ws_f2 = load_excel_files(uploaded_f1, uploaded_f2)
            clean_and_merge_columns(ws_f1)

            ws_f1["H11"].value = "N° de palette"
            copy_cell_style(ws_f1["G11"], ws_f1["H11"])

            fill_palette_number(ws_f1, ws_f2)

            output: BytesIO = save_workbook_to_bytes(wb_f1)

            st.download_button(
                label="Télécharger packing list excel",
                data=output.getvalue(),
                file_name="PackingList.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.error(f"❌ Une erreur est survenue : {e}")


if __name__ == "__main__":
    main()
