import streamlit as st
from applications import packing_list
from applications import nouvel_outil
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Outils e-LOG",
    page_icon="📦",
    layout="centered"
)

# Affichage du logo
st.image("logo_marketparts.png", width=200)

# Titre principal
st.title("Bienvenue dans l’outil e-LOG")
st.markdown("### Veuillez choisir un outil ci-dessous 👇")

# Séparateur
st.markdown("---")

# Deux colonnes pour les boutons
col1, col2 = st.columns(2)

with col1:
    if st.button("🧾 Générateur de Packing List"):
        packing_list.run()

with col2:
    if st.button("🆕 Nouvel outil (F3 / F4)"):
        nouvel_outil.run()
