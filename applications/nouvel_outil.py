import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.drawing.image import Image as OpenpyxlImage
from openpyxl.worksheet.properties import WorksheetProperties, PageSetupProperties
from io import BytesIO
from PIL import Image
import tempfile


def run():
    st.title("🆕 Traitement personnalisé F1 + F2")

    # Upload fichiers F1 et F2
    col1, col2 = st.columns(2)
    with col1:
        uploaded_f1 = st.file_uploader("📁 Fichier F1 (TO SHIP)", type=["xlsx"], key="f1")
    with col2:
        uploaded_f2 = st.file_uploader("📁 Fichier F2 (E LOG)", type=["xlsx"], key="f2")

    if uploaded_f1 and uploaded_f2:
        try:
            temp_f1 = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            temp_f1.write(uploaded_f1.read())
            temp_f1.seek(0)

            temp_f2 = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            temp_f2.write(uploaded_f2.read())
            temp_f2.seek(0)

            wb_f1 = load_workbook(temp_f1.name)
            ws_f1 = wb_f1.active
            df_f2 = pd.read_excel(temp_f2.name, sheet_name=0)

            # Identifier dynamiquement la ligne d'en-tête contenant "N° COLIS"
            header_row_idx = None
            for i, row in enumerate(ws_f1.iter_rows(min_row=1, max_row=30), start=1):
                if any(cell.value == "N° COLIS" for cell in row):
                    header_row_idx = i
                    break

            if header_row_idx is None:
                st.error("❌ Erreur : 'N° COLIS' n'a pas été trouvé dans le fichier F1.")
                return

            headers = [cell.value for cell in ws_f1[header_row_idx]]
            col_n_colis = headers.index("N° COLIS") + 1
            col_n_palette = headers.index("N° PALETTE") + 1
            col_fournisseur = headers.index("Fournisseur") + 1

            # Nettoyage et mapping depuis F2
            df_f2["Package Number"] = df_f2["Package Number"].astype(str).str.strip()
            df_f2["N° pal "] = df_f2["N° pal "]
            colis_to_palette = dict(zip(df_f2["Package Number"], df_f2["N° pal "]))

            for row in ws_f1.iter_rows(min_row=header_row_idx+1, max_row=ws_f1.max_row):
                colis_val = str(row[col_n_colis - 1].value).strip() if row[col_n_colis - 1].value else None
                if colis_val in colis_to_palette:
                    row[col_n_palette - 1].value = colis_to_palette[colis_val]
                row[col_fournisseur - 1].value = "MARKETPARTS"

            f1_colis = [str(row[col_n_colis - 1].value).strip() for row in ws_f1.iter_rows(min_row=header_row_idx+1, max_row=ws_f1.max_row) if row[col_n_colis - 1].value]
            f2_colis = df_f2["Package Number"].dropna().astype(str).str.strip().tolist()
            missing_in_f2 = sorted(set(f1_colis) - set(f2_colis))
            missing_in_f1 = sorted(set(f2_colis) - set(f1_colis))

            if missing_in_f2 or missing_in_f1:
                st.warning("\n".join([
                    "\n\n### ⚠️ Incohérences détectées :",
                    f"- {len(missing_in_f2)} colis présents dans F1 mais absents de F2 : {', '.join(missing_in_f2) if missing_in_f2 else 'Aucun'}",
                    f"- {len(missing_in_f1)} colis présents dans F2 mais absents de F1 : {', '.join(missing_in_f1) if missing_in_f1 else 'Aucun'}"
                ]))

            for row in ws_f1.iter_rows(min_row=header_row_idx, max_row=ws_f1.max_row):
                for cell in row:
                    if cell.value:
                        cell.alignment = Alignment(horizontal="center", vertical="center")

            for col in range(1, 16):
                cell = ws_f1.cell(row=header_row_idx, column=col)
                cell.fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")
                cell.font = Font(color="FFFFFF", bold=True)

            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            for row in ws_f1.iter_rows(min_row=header_row_idx, max_row=ws_f1.max_row, min_col=1, max_col=15):
                for cell in row:
                    cell.border = thin_border

            ws_f1.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
            ws_f1.page_setup.fitToWidth = 1
            ws_f1.page_setup.fitToHeight = 0
            ws_f1.print_title_rows = f"{header_row_idx}:{header_row_idx}"
            ws_f1.oddFooter.center.text = "Page &[Page] / &[Pages]"

            for col in ws_f1.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                ws_f1.column_dimensions[column].width = max_length + 2

            try:
                logo_path = "logo_marketparts.png"
                logo = OpenpyxlImage(logo_path)
                logo.width = int(logo.width * 0.36)
                logo.height = int(logo.height * 0.36)
                ws_f1.add_image(logo, "A1")
            except:
                pass

            output = BytesIO()
            wb_f1.save(output)
            output.seek(0)

            st.success("✅ Traitement terminé.")
            st.download_button(
                label="📥 Télécharger le fichier traité",
                data=output,
                file_name="PackingList_Traitée.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"❌ Erreur : {e}")
