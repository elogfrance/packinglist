import streamlit as st

# ➋ Configuration de la page (toujours en premier)
st.set_page_config(page_title="Outils E-LOG", layout="centered")

# ➊ Récupérer le paramètre 'tool' via l'API stable
tool = st.query_params.get("tool", [None])[0]

# ➌ Routing selon le paramètre 'tool'
if tool == "packing_list":
    import applications.packing_list as pl
    pl.run()

elif tool == "autodoc":
    import applications.packing_list_autodoc as autodoc
    autodoc.run()

else:
    # Menu principal par boutons
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
            # On utilise l'API expérimentale pour écrire le paramètre
            st.experimental_set_query_params(tool="packing_list")
            st.experimental_rerun()

    with col2:
        if st.button("🧾 Packing List Autodoc"):
            st.experimental_set_query_params(tool="autodoc")
            st.experimental_rerun()
