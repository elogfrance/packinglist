import streamlit as st
from applications import packing_list, nouvel_outil
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Outils e-LOG",
    page_icon="📦",
    layout="centered"
)

# Initialisation de l'état de l'outil sélectionné
if "outil" not in st.session_state:
    st.session_state.outil = None

# === AUCUN OUTIL SÉLECTIONNÉ : PAGE D’ACCUEIL ===
if st.session_state.outil is None:
    st.image("logo_marketparts.png", width=200)
    st.title("Bienvenue dans l’outil e-LOG")
    st.markdown("### Veuillez choisir un outil 👇")
    st.markdown("---")

    if st.button("🧾 Générateur de Packing List", key="bouton_packing"):
        st.session_state.outil = "packing"
        st.rerun()

    if st.button("🆕 Nouvel outil (F3 / F4)", key="bouton_nouvel"):
        st.session_state.outil = "nouvel"
        st.rerun()

# === OUTIL : PACKING LIST ===
elif st.session_state.outil == "packing":
    if st.button("⬅️ Retour à l’accueil", key="retour_packing"):
        st.session_state.outil = None
        st.rerun()
    packing_list.run()

# === OUTIL : NOUVEL OUTIL ===
elif st.session_state.outil == "nouvel":
    if st.button("⬅️ Retour à l’accueil", key="retour_nouvel"):
        st.session_state.outil = None
        st.rerun()
    nouvel_outil.run()

