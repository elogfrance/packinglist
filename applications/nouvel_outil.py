# === VÉRIFICATION VISUELLE DES CORRESPONDANCES ===
try:
    def normalize(val):
        return str(val).strip().replace('\xa0', '').replace('\n', '').replace('\r', '').lower()

f1_series = df1["Package Number"].dropna().astype(str).map(normalize)
f1_series = f1_series[f1_series != 'nan']
f2_series = df2["Package Number"].dropna().astype(str).map(normalize)
f2_series = f2_series[f2_series != 'nan']



    f1_values = set(f1_series)
    f2_values = set(f2_series)

    only_in_f1 = sorted(f1_values - f2_values)
    only_in_f2 = sorted(f2_values - f1_values)

    if only_in_f1 or only_in_f2:
        st.markdown("### ⚠️ Résumé des écarts entre F1 et F2")
        st.markdown("---")

    if only_in_f1:
        st.markdown(
            f"""
            <div style="background-color:#ff4d4d;padding:16px;border-radius:8px;color:white;">
                <strong>❌ {len(only_in_f1)} document(s) trouvés dans F1 mais absents de F2</strong><br>
                Exemples : {", ".join(only_in_f1[:10])}{'...' if len(only_in_f1) > 10 else ''}
            </div>
            """, unsafe_allow_html=True)

    if only_in_f2:
        st.markdown(
            f"""
            <div style="background-color:#fff3cd;padding:16px;border-radius:8px;color:#856404;">
                <strong>⚠️ {len(only_in_f2)} package(s) trouvés dans F2 mais absents de F1</strong><br>
                Exemples : {", ".join(only_in_f2[:10])}{'...' if len(only_in_f2) > 10 else ''}
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Erreur lors de la vérification des correspondances F1/F2 : {e}")
