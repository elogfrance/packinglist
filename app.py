import streamlit as st

# ➋ Configuration de la page (toujours en tout premier)
st.set_page_config(page_title="Outils E-LOG", layout="centered")

# ➊ Initialisation de session_state['tool']
if "tool" not in st.session_state:
    st.session_state.tool = None

# ➌ Routing selon session_state.tool
if st.session_state.tool == "packing_list":
    import applications.packing_list as pl
    pl.run()
    st.stop()

elif st.session_state.tool == "autodoc":
    import applications.packing_list_autodoc as autodoc
    autodoc.run()
    st.stop()

#  Menu principal
st.markdown(
    "<h1 style='text-align: center; color: #3a4e9f;'>🧰 Outils E-LOG</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Choisissez un outil :</p>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    if st.button("📦 Packing List"):
        st.session_state.tool = "packing_list"
with col2:
    if st.button("🧾 Packing List Autodoc"):
        st.session_state.tool = "autodoc"
