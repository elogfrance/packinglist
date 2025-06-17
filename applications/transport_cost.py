import streamlit as st
from applications import packing_list, nouvel_outil, transport_cost  # Import des modules

# Configuration de la page
st.set_page_config(
    page_title="Outils e-LOG",
    page_icon="📦",
    layout="centered"
)

# Initialisation de l’état
if "outil" not in st.session_state:
    st.session_state.outil = None

# Page d’accueil si aucun outil sélectionné
if st.session_state.outil is None:
    st.image("logo_marketparts.png", width=200)
    st.title("Bienvenue dans l’outil e-LOG")
    st.markdown("### Veuillez choisir un outil 👇")
    st.markdown("---")

    if st.button("🧾 Générateur de Packing List"):
        st.session_state.outil = "packing"
        st.rerun()

    if st.button("🆕 Nouvel outil"):
        st.session_state.outil = "nouvel"
        st.rerun()

    if st.button("🚚 Coûts de transport"):
        st.session_state.outil = "transport"
        st.rerun()

# Redirection vers l’outil sélectionné
if st.session_state.outil == "packing":
    packing_list.run()

elif st.session_state.outil == "nouvel":
    nouvel_outil.run()

elif st.session_state.outil == "transport":
    transport_cost.main()
