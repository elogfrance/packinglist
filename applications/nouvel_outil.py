import streamlit as st
import pandas as pd
import re
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image as OpenpyxlImage
from openpyxl.worksheet.properties import WorksheetProperties, PageSetupProperties
from io import BytesIO
import tempfile

def run():
    st.title("Générateur Packing List Autodoc")

    # Upload des fichiers F1 et F2
    f1 = st.file_uploader("📁 Fichier F1 (TO SHIP)", type=["xlsx"], key="f1")
    f2 = st.file_uploader("📁 Fichier F2 (E LOG)", type=["xlsx"], key="f2")

    if f1 and f2:
        try:
            # Chargement fichiers temporaires
            temp_f1 = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            temp_f1.write(f1.read())
            temp_f1.seek(0)
            temp_f2 = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            temp_f2.write(f2.read())
            temp_f2.seek(0)

            df_f1 = pd.read_excel(temp_f1.name)
            df_f2 = pd.read_excel(temp_f2.name)

            # === Ici : traitement et transformation de df_f1 / df_f2 ===
            # ... suppression de colonnes, nettoyage, enrichissements...
            # ... mise en forme Excel, logo, etc. (ton code habituel ici)

            # Exemple de sauvegarde
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Packing List"
            ws["A1"] = "Ceci est un exemple"

            # === INSERTION VÉRIFICATION DE CORRESPONDANCE ===
            try:
                f1_values = set(df_f1["Document number"].dropna().astype(str).str.strip())
                f2_values = set(df_f2["Package Number"].dropna().astype(str).str.strip())

                only_in_f1 = f1_values - f2_values
                only_in_f2 = f2_values - f1_values

                if only_in_f1:
                    st.warning("⚠️ Attention : les documents suivants sont dans F1 mais absents de F2 :")
                    st.write(sorted(only_in_f1))

                if only_in_f2:
                    st.warning("⚠️ Attention : les packages suivants sont dans F2 mais absents de F1 :")
                    st.write(sorted(only_in_f2))

            except Exception as e:
                st.error(f"Erreur lors de la vérification des correspondances F1/F2 : {e}")

            # === Export final ===
            output = BytesIO()
            wb.save(output)
            st.download_button(
                label="📥 Télécharger le fichier final",
                data=output.getvalue(),
                file_name="packing_list_final.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"Erreur : {e}")
