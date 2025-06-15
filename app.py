import streamlit as st

# ➊ Récupérer le paramètre 'tool' dans l'URL
tool = st.query_params.get("tool", [None])[0]

# ➋ Configuration de la page
st.set_page_config(page_title="Outils E-LOG", layout="centered")

# ➌ Routing selon le paramètre 'tool'
if tool == "packing_list":
    import applications.packing_list as pl
    pl.run()

elif tool == "autodoc":
    import applications.packing_list_autodoc as autodoc
    autodoc.run()

else:
    # Menu principal par vignettes
    st.markdown(
        "<h1 style='text-align: center; color: #3a4e9f;'>🧰 Outils E-LOG</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center;'>Cliquez sur une vignette pour ouvrir l’outil dans un nouvel onglet :</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # Vignette Packing List
    link1 = (
        '<a href="./?tool=packing_list" target="_blank" style="text-decoration: none;">'
        '<div style="padding:20px; text-align:center; border:1px solid #ddd; '
        'border-radius:8px;">'
        '📦<br><strong>Packing List</strong>'
        '</div></a>'
    )

    # Vignette Packing List Autodoc
    link2 = (
        '<a href="./?tool=autodoc" target="_blank" style="text-decoration: none;">'
        '<div style="padding:20px; text-align:center; border:1px solid #ddd; '
        'border-radius:8px;">'
        '🧾<br><strong>Packing List Autodoc</strong>'
        '</div></a>'
    )

    col1.markdown(link1, unsafe_allow_html=True)
    col2.markdown(link2, unsafe_allow_html=True)
