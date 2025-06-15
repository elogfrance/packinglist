import streamlit as st

st.set_page_config(page_title="Outils E-LOG", layout="centered")

st.markdown("<h1 style='text-align: center; color: #3a4e9f;'>🧰 Outils E-LOG</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choisissez un outil à lancer :</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("📦 Packing List"):
        import apps.packing_list as pl
        pl.run()

with col2:
    if st.button("🧾 Packing List Autodoc"):
        import apps.packing_list_autodoc as autodoc
        autodoc.run()
