import streamlit as st
from applications import packing_list, nouvel_outil
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="Outils e-LOG", page_icon="📦", layout="centered")

# Gestion de la "page" active
if "page" not in st.session_state:
    st.session_state.page = "home"

# Page d'accueil
if st.session_state.page == "home":
    st.image("logo_marketparts.png", width=400)
    st.markdown("### Veuillez choisir un outil 👇")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Packing List"):
            st.session_state.page = "packing"

    with col2:
        if st.button("Packing liste autodoc"):
            st.session_state.page = "nouvel"

# Page : Packing list
elif st.session_state.page == "packing":
    if st.button("⬅️ Retour à l'accueil"):
        st.session_state.page = "home"
    packing_list.run()

# Page : Nouvel outil
elif st.session_state.page == "nouvel":
    if st.button("⬅️ Retour à l'accueil"):
        st.session_state.page = "home"
    nouvel_outil.run()
