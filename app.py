import streamlit as st
from applications import packing_list, nouvel_outil
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Outils e-LOG",
    page_icon="📦",
    layout="centered"
)

# Logo
st.image("logo_marketparts.png", width=200)

# Titre
st.title("Bienvenue dans l’outil e-LOG")
st.markdown("### Veuillez choisir un outil 👇")
st.markdown("---")

# Affichage des boutons l'un après l'autre
if st.button("🧾 Générateur de Packing List"):
    st.markdown("### 🧾 Générateur de Packing List")
    packing_list.run()

elif st.button("🆕 Nouvel outil (F3 / F4)"):
    st.markdown("### 🆕 Nouvel outil (F3 / F4)")
    nouvel_outil.run()
