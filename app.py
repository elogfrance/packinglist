import streamlit as st
from applications import packing_list, nouvel_outil
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Outils e-LOG",
    page_icon="📦",
    layout="centered"
)

# --- Gestion d’état de navigation (stocké localement) ---
if "outil" not in st.session_state:
    st.session_state.outil = None

# --- Si aucun outil sélectionné : page d’accueil ---
if st.session_state.outil is None:
    st.image("logo_marketparts.png", width=200)
    st.title("Bienvenue dans l’outil e-LOG")
    st.markdown("### Veuillez choisir un outil 👇")
    st.markdown("---")

    if st.button("🧾 Générateur de Packing List"):
        st.session_state.outil = "packing"
        st.rerun()

    elif st.button("🆕 Nouvel outil (F3 / F4)"):
        st.session_state.outil = "nouvel"
        st.rerun()

# --- Si un outil a été sélectionné, on l’affiche seul ---
elif st.session_state.outil == "packing":
    if st.button("⬅️ Retour à l’accueil"):
        st.session_state.outil = None
        st.rerun()
    packing_list.run()

elif st.session_state.outil == "nouvel":
    if st.button("⬅️ Retour à l’accueil"):
        st.session_state.outil = None
        st.rerun()
    nouvel_outil.run()
