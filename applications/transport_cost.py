import streamlit as st
import pandas as pd
import math
from pathlib import Path

# ------------------------------------------------------------------
# Localisation de la grille Excel (dossier data/)
# ------------------------------------------------------------------
TARIF_PATH = Path(__file__).resolve().parent.parent / "data" / "tarifs_merged.xlsx"

# ------------------------------------------------------------------
# Frais fixes et optionnels
# ------------------------------------------------------------------
FIXED_FEES_DEFAULT = {
    "Terme fixe administratif (EDI)": 3.51,
    "Risk Fee": 1.98,
}

OPTIONAL_FEES = {
    "Produits dangereux (base)": 18.54,
    "RDV tél. (manuel)": 15.80,
}

DG_EXTRA = {        # surcoûts produits dangereux
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
    """Charge la grille tarifaire stockée dans data/tarifs_merged.xlsx."""
    if not TARIF_PATH.exists():
        st.error(f"Grille tarifaire introuvable : {TARIF_PATH}")
        st.stop()
    return pd.read_excel(TARIF_PATH, sheet_name=0)


def arrondi_dizaine_superieure(val: float) -> int:
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
        upper = float(col.split(" kg")[0].split("-")[1])
        if poids <= upper:
            return row[col]
    return None

# ------------------------------------------------------------------
# Interface Streamlit – Méthode « Coûts export »
# ------------------------------------------------------------------
def main():
    st.title("📦 Calcul des Coûts export (HT)")

    # 1) Charger la grille depuis /data
    df_tar = load_tariff()
    st.markdown(
        f"Grille tarifaire chargée (**{len(df_tar):,} lignes**). "
        "Renseignez votre destination et vos paramètres :"
    )

    # 2) Formulaire
    with st.form("form"):
        col1, col2 = st.columns(2)

        with col1:
            pays = st.text_input("Pays", value="France")
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

    # 3) Calcul transport
    poids_arr = arrondi_dizaine_superieure(poids_input)
    tarif = find_tariff(df_tar, pays, zone, poids_arr)
    if tarif is None or pd.isna(tarif):
        st.error("Tarif introuvable pour cette destination / zone.")
        return

    fret_ht = (poids_arr / 100.0) * tarif
    fuel_ht = fret_ht * fuel_pct / 100.0

    # 4) Frais fixes + options
    frais = FIXED_FEES_DEFAULT.copy()

    if opt_dg:
        montant_dg = OPTIONAL_FEES["Produits dangereux (base)"]
        for key, extra in DG_EXTRA.items():
            if pays.strip().lower().startswith(key.lower()):
                montant_dg += extra
                break
        frais["Produits dangereux"] = montant_dg

    if opt_rdv:
        frais["RDV tél. (manuel)"] = OPTIONAL_FEES["RDV tél. (manuel)"]

    total_frais = sum(frais.values())

    # 5) Minimum de perception
    sous_total_ht = fret_ht + fuel_ht + total_frais
    if sous_total_ht < MIN_PERCEPTION:
        frais["Minimum de perception"] = MIN_PERCEPTION - sous_total_ht
        total_frais = sum(frais.values())
        sous_total_ht = fret_ht + fuel_ht + total_frais

    total_ht = sous_total_ht

    # 6) Affichage
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

        df_lignes = pd.DataFrame(
            lignes, columns=["Libellé", "Unitaire", "Qté/Coef.", "Montant € HT"]
        )
        st.table(df_lignes)
        st.write(f"**Total HT : {total_ht:,.2f} €**")


if __name__ == "__main__":
    main()
