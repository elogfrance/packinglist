import streamlit as st
# ➊ Récupérer le paramètre 'tool' dans l'URL
params = st.experimental_get_query_params()
tool = params.get("tool", [None])[0]


# ➌ Routing selon le paramètre 'tool'
if tool == "packing_list":
    import applications.packing_list as pl
    pl.run()

elif tool == "autodoc":
    import applications.packing_list_autodoc as autodoc
    autodoc.run()

else:
    # Menu principal
    st.markdown(
        "<h1 style='text-align: center; color: #3a4e9f;'>🧰 Outils E-LOG</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center;'>Cliquez sur une vignette pour ouvrir l’outil dans un nouvel onglet :</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    # On ajoutera les liens à l’étape suivante


st.markdown(
    "<h1 style='text-align: center; color: #3a4e9f;'>🧰 Outils E-LOG</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Choisissez un outil à lancer :</p>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    if st.button("📦 Packing List"):
        import applications.packing_list as pl
        pl.run()

with col2:
    if st.button("🧾 Packing List Autodoc"):
        import applications.packing_list_autodoc as autodoc
        autodoc.run()
