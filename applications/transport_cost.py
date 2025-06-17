import streamlit as st
import pandas as pd
import math
from pathlib import Path

# ------------------------------------------------------------------
# Chemin vers la grille tarifaire
# ------------------------------------------------------------------
TARIF_PATH = Path(__file__).resolve().parent.parent / "data" / "tarifs_merged.xlsx"

# ------------------------------------------------------------------
# Barème de frais
# ------------------------------------------------------------------
FIXED_FEES_DEFAULT = {
    "Terme fixe administratif (EDI)": 3.51,
    "Risk Fee": 1.98,
}

OPTIONAL_FEES = {
    "Produits dangereux (base)": 18.54,
    "RDV tél. (manuel)": 15.80,
}

DG_EXTRA = {
    "GB": 60.02,
    "Finlande": 33.92,
    "Norvège": 33.92,
    "Suède": 33.92,
    "Italie": 33.92,
}

MIN_PERCEPTION = 75.0  # € HT
VOL_FACTOR = 250       # kg/m3
FUEL_PCT = 10.0        # surcharge carburant fixe

# ------------------------------------------------------------------
@st.cache_data
def load_tariff() -> pd.DataFrame:
    if not TARIF_PATH.exists():
        st.error(f"Grille tarifaire introuvable : {TARIF_PATH}")
        st.stop()
    return pd.read_excel(TARIF_PATH, sheet_name=0)


def arrondi_dizaine_sup(val: float) -> int:
    return int(math.ceil(val / 10.0) * 10)


def find_tariff(df: pd.DataFrame, pays: str, zone: str, poids: int) -> float | None:
    mask = (
        df["Pays"].str.contains(pays, case=False, na=False)
        & (df["Zone"].astype(str) == str(zone))
    )
    if not mask.any():
        return None

    row = df.loc[mask].iloc[0]
    cols = []
    for c in df.columns:
        if c.endswith("kg") and "-" in c:
            try:
                upper = float(c.split(" kg")[0].split("-")[1])
                cols.append((upper, c))
            except ValueError:
                continue
    if not cols:
        return None
    cols.sort(key=lambda x: x[0])
    for upper, col in cols:
        if poids <= upper:
            return row[col]
    return None

# ------------------------------------------------------------------
# App principale
# ------------------------------------------------------------------

def main():
    st.title("📦 Coûts export – Saisie palettes (HT)")

    df_tar = load_tariff()
    pays_liste = sorted(df_tar["Pays"].dropna().unique())

    with st.form("form"):
        col1, col2 = st.columns(2)
        with col1:
            pays = st.selectbox("Pays", pays_liste, index=pays_liste.index("France") if "France" in pays_liste else 0)
            zones_pays = sorted(df_tar.loc[df_tar["Pays"].str.contains(pays, case=False, na=False), "Zone"].astype(str).unique())
            zone = st.selectbox("Zone (CP / code zone)", zones_pays)
        with col2:
            st.markdown(f"Surcharge carburant fixe : **{FUEL_PCT:.1f}%**")
            opt_dg = st.checkbox("Produits dangereux")
            opt_rdv = st.checkbox("RDV tél. (manuel)")

        st.markdown("### Palettes (dimensions en cm & poids réel en kg)")
        demo_df = pd.DataFrame({"Long(cm)": [80], "Larg(cm)": [120], "Haut(cm)": [100], "Poids(kg)": [100]})
        data = st.data_editor(demo_df, num_rows="dynamic", use_container_width=True, key="palettes")

        submitted = st.form_submit_button("💰 Calculer")

    if not submitted:
        return

    data = data.dropna(how="all")
    if data.empty:
        st.error("Merci de saisir au moins une palette.")
        return
    try:
        data_numeric = data.astype(float)
    except ValueError:
        st.error("Toutes les valeurs doivent être numériques.")
        return

    vols_m3 = (data_numeric["Long(cm)"] / 100) * (data_numeric["Larg(cm)"] / 100) * (data_numeric["Haut(cm)"] / 100)
    poids_vol = vols_m3 * VOL_FACTOR
    poids_reel = data_numeric["Poids(kg)"]

    total_reel = poids_reel.sum()
    total_vol = poids_vol.sum()
    poids_taxable = max(total_reel, total_vol)
    poids_arr = arrondi_dizaine_sup(poids_taxable)

    tarif = find_tariff(df_tar, pays, zone, poids_arr)
    if tarif is None or pd.isna(tarif):
        st.error("Tarif introuvable pour cette destination / zone.")
        return

    fret_ht = (poids_arr / 100.0) * tarif
    fuel_ht = fret_ht * FUEL_PCT / 100.0

    frais = FIXED_FEES_DEFAULT.copy()
    if opt_dg:
        montant_dg = OPTIONAL_FEES["Produits dangereux (base)"]
        for key, extra in DG_EXTRA.items():
            if pays.lower().startswith(key.lower()):
                montant_dg += extra
                break
        frais["Produits dangereux"] = montant_dg
    if opt_rdv:
        frais["RDV tél. (manuel)"] = OPTIONAL_FEES["RDV tél. (manuel)"]

    total_frais = sum(frais.values())
    sous_total_ht = fret_ht + fuel_ht + total_frais
    if sous_total_ht < MIN_PERCEPTION:
        frais["Minimum de perception"] = MIN_PERCEPTION - sous_total_ht
        total_frais = sum(frais.values())
        sous_total_ht = fret_ht + fuel_ht + total_frais

    total_ht = sous_total_ht

    # Affichage
    st.header("Résultat – Coûts export (HT)")
    st.write(f"**Poids réel total : {total_reel:.2f} kg**")
    st.write(f"**Poids volumétrique total : {total_vol:.2f} kg**")
    st.write(f"**Poids taxable arrondi : {poids_arr} kg**")
    st.success(f"**TOTAL HT À FACTURER : {total_ht:,.2f} €**")

    with st.expander("🧾 Détail complet HT"):
        lignes = [
            ["Fret (tarif tranche)", f"{tarif:,.2f} €/100 kg", poids_arr / 100, fret_ht],
            [f"Surcharge carburant {FUEL_PCT:.1f}%", "—", "—", fuel_ht],
        ]
        for lib, montant in frais.items():
            lignes.append([lib, "", "", montant])
        st.table(pd.DataFrame(lignes, columns=["Libellé", "Unitaire", "Qté/Coef.", "Montant € HT"]))
        st.markdown("**Données palettes :**")
        st.dataframe(data_numeric.reset_index(drop=True))


if __name__ == "__main__":
    main()
