import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Générateur de Packing List", layout="wide")
from PIL import Image

# Afficher le logo
logo = Image.open("logo v3.png")
st.image(logo, width=200)

# Titre personnalisé
st.markdown(
    "<h1 style='color:#3a4e9f;'>📦 Générateur de Packing List</h1>",
    unsafe_allow_html=True

)

uploaded_file = st.file_uploader("📁 Importer un fichier Excel ou CSV", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("🧾 Aperçu des données importées")
    st.dataframe(df)

    regroupement = st.selectbox("Regrouper les lignes par :", options=["Commande", "Client"])

    if regroupement in df.columns:
        grouped = df.groupby(df[regroupement])

        st.subheader("📄 Packing Lists générées")

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            for key, group in grouped:
                st.markdown(f"### 📦 {regroupement} : {key}")
                st.dataframe(group)
                group.to_excel(writer, sheet_name=str(key)[:31], index=False)
            writer.save()

        st.download_button(
            label="📥 Télécharger toutes les packing lists (Excel)",
            data=buffer,
            file_name="packing_lists.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning(f"❌ La colonne '{regroupement}' n’existe pas dans vos données.")
