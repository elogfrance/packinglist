import streamlit as st
import pandas as pd
import math
from pathlib import Path

# ------------------------------------------------------------------
# Chemin vers la grille Excel
# ------------------------------------------------------------------
TARIF_PATH = Path(__file__).resolve().parent.parent / "data" / "tarifs_merged.xlsx"

# ------------------------------------------------------------------
# Barème des frais fixes et optionnels
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

# ------------------------------------------------------------------
# Fonctions utilitaires
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
    cols = [c for c in df.columns if c.endswith("kg") and "-" in c]
    cols.sort(key=lambda c: float(c.split(" kg")[0].split("-")[1]))

    for col in cols:
        if poids <= float(col.split(" kg")[0].split("-")[1]):
            return row[col]
    return None

# ------------------------------------------------------------------
# Interface Streamlit – Méthode « Coûts export »
# ------------------------------------------------------------------
def main():
    st.title("📦 Calcul des Coûts export (HT)")

    df_tar = load_tariff()
    pays_liste = sorted(df_tar["Pays"].dropna().unique())

    st.markdown(
        f"Grille tarifaire chargée (**{len(df_tar):,} lignes**). "
        "Renseignez votre destination et vos paramètres :"
    )

    with st.form("form"):
        col1, col2 = st.columns(2)

        with col1:
            pays = st.selectbox("Pays", pays_liste, index=pays_liste.index("France") if "France" in pays_liste else 0)
            zone = st.text_input("Zone (CP / code zone)", value="69")
            poids_input = st.number_input(
                "Poids taxable ou réel (kg)", min_value=0.0, value=350.0, step=0.1
            )
            fuel_pct = st.number_input(
                "Surcharge carburant (%)", min_value=0.0, value=10.0, step=0.1
            )

        with col2:
            st.markdown("### Options")
            opt_dg = st.checkbox("Produits dangereux")
            opt_rdv = st.checkbox("Prise de RDV tél. manuel")

        submitted = st.form_submit_button("💰 Calculer")

    if not submitted:
        return

    # ---------------- Calcul transport ----------------
    poids_arr = arrondi_dizaine_sup(poids_input)
    tarif = find_tariff(df_tar, pays, zone, poids_arr)
    if tarif is None or pd.isna(tarif):
        st.error("Tarif introuvable pour cette destination / zone.")
        return

    fret_ht = (poids_arr / 100.0) * tarif
    fuel_ht = fret_ht * fuel_pct / 100.0

    # --------------- Frais fixes + options ------------
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

    # ---------------- Affichage -----------------------
    st.header("Résultat – Coûts export (HT)")
    st.write(f"**Poids taxable arrondi : {poids_arr} kg**")
    st.success(f"**TOTAL HT À FACTURER : {total_ht:,.2f} €**")

    with st.expander("🧾 Détail complet HT"):
        lignes = [
            ["Fret (tarif tranche)", f"{tarif:,.2f} €/100 kg", poids_arr / 100, fret_ht],
            [f"Surcharge carburant {fuel_pct:.1f}%", "—", "—", fuel_ht],
        ]
        for lib, montant in frais.items():
            lignes.append([lib, "", "", montant])

        st.table(pd.DataFrame(lignes, columns=["Libellé", "Unitaire", "Qté/Coef.", "Montant € HT"]))
        st.write(f"**Total HT : {total_ht:,.2f} €**")


if __name__ == "__main__":
    main()
