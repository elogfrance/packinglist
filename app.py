import streamlit as st
from applications import packing_list, nouvel_outil
from PIL import Image

st.set_page_config(page_title="Outils e-LOG", page_icon="📦", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

# Page d'accueil
if st.session_state.page == "home":
    st.image("logo_marketparts.png", width=200)
    st.title("Bienvenue dans l’outil e-LOG")
    st.markdown("### Veuillez choisir un outil 👇")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧾 Générateur de Packing List"):
            st.session_state.page = "packing"
            st.experimental_rerun()  # 🔁 recharge immédiate

    with col2:
        if st.button("🆕 Nouvel outil (F3 / F4)"):
            st.session_state.page = "nouvel"
            st.experimental_rerun()  # 🔁 recharge immédiate

# Page : Packing list
elif st.session_state.page == "packing":
    if st.button("⬅️ Retour à l'accueil"):
        st.session_state.page = "home"
        st.experimental_rerun()
    packing_list.run()

# Page : Nouvel outil
elif st.session_state.page == "nouvel":
    if st.button("⬅️ Retour à l'accueil"):
        st.session_state.page = "home"
        st.experimental_rerun()
    nouvel_outil.run()
