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

# Titre de l'application
st.title("Bienvenue dans l’outil e-LOG")
st.markdown("### Veuillez choisir un module à utiliser ci-dessous :")

# Menu de sélection
choix = st.selectbox(
    "📌 Sélectionnez l’outil à lancer :",
    [
        "🔹 Générateur de packing list",
        "🆕 Nouvel outil (F3 / F4)"
    ]
)

# Redirection dynamique vers le module choisi
if choix == "🔹 Générateur de packing list":
    packing_list.run()

elif choix == "🆕 Nouvel outil (F3 / F4)":
    nouvel_outil.run()
