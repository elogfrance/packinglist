import streamlit as st
from applications import packing_list, nouvel_outil
from PIL import Image

st.set_page_config(page_title="Outils e-LOG", page_icon="📦", layout="centered")

st.image("logo_marketparts.png", width=200)
st.title("Bienvenue dans l’outil e-LOG")
st.markdown("### Veuillez choisir un outil 👇")
st.markdown("---")

# Deux colonnes pour les boutons
col1, col2 = st.columns(2)

# Drapeaux de déclenchement
launch_tool = None

with col1:
    if st.button("🧾 Générateur de Packing List"):
        launch_tool = "packing"

with col2:
    if st.button("🆕 Nouvel outil (F3 / F4)"):
        launch_tool = "nouvel"

# Lancement du bon outil immédiatement après le clic
if launch_tool == "packing":
    packing_list.run()

elif launch_tool == "nouvel":
    nouvel_outil.run()
