import streamlit as st
from applications import packing_list, nouvel_outil, transport_cost    # + import
from PIL import Image

# ------------------------------------------------
# Configuration de la page
# ------------------------------------------------
st.set_page_config(
    page_title="Outils e-LOG",
    page_icon="📦",
    layout="centered"
)

# ------------------------------------------------
# Initialisation de l’état d’affichage
# ------------------------------------------------
if "outil" not in st.session_state:
    st.session_state.outil = None

# ------------------------------------------------
# Page d’accueil (aucun outil sélectionné)
# ------------------------------------------------
if st.session_state.outil is None:
    st.image("logo_marketparts.png", width=600)

    st.markdown("### Veuillez choisir un outil 👇")
    st.markdown("---")

    # 1) Générateur de packing-list
    if st.button("Générateur de Packing List standard", key="bouton_packing"):
        st.session_state.outil = "packing"
        st.rerun()

    # 2) Nouvel outil (F3 / F4)
    if st.button("Générateur de Packing List Autodoc", key="bouton_nouvel"):
        st.session_state.outil = "nouvel"
        st.rerun()

    # 3) Coûts export  ← NEW
    if st.button("Coûts Transport", key="bouton_export"):
        st.session_state.outil = "export"
        st.rerun()

# ------------------------------------------------
# Générateur de packing-list
# ------------------------------------------------
elif st.session_state.outil == "packing":
    if st.button("⬅️ Retour à l’accueil", key="retour_packing"):
        st.session_state.outil = None
        st.rerun()
    packing_list.run()

# ------------------------------------------------
# Nouvel outil (F3 / F4)
# ------------------------------------------------
elif st.session_state.outil == "nouvel":
    if st.button("⬅️ Retour à l’accueil", key="retour_nouvel"):
        st.session_state.outil = None
        st.rerun()
    nouvel_outil.run()

# ------------------------------------------------
# Coûts export  ← NEW
# ------------------------------------------------
elif st.session_state.outil == "export":
    if st.button("⬅️ Retour à l’accueil", key="retour_export"):
        st.session_state.outil = None
        st.rerun()
    transport_cost.main()
