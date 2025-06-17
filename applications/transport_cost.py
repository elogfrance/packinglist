import streamlit as st
import pandas as pd
import math
from pathlib import Path

# ------------------------------------------------------------------
# FICHIER TARIFS (Excel fusionné dans data/)
# ------------------------------------------------------------------
TARIF_PATH = Path(__file__).resolve().parent.parent / "data" / "tarifs_merged.xlsx"

# Paramètres globaux
VOL_FACTOR = 250      # kg / m³
FUEL_PCT   = 10.0     # surcharge carburant fixe
MIN_PERCEPTION = 75.0 # € HT

# Frais fixes (toujours appliqués)
FIXED_FEES = {
    "Terme fixe administratif": 3.51,
    "Risk Fee": 1.98,
}

# Options facultatives
OPTIONAL_FEES_BASE = {
    "Produits dangereux (base)": 18.54,
    "RDV tél. (manuel)": 15.80,
}

DG_EXTRA = {  # majorations MD selon pays
    "GB": 60.02,
    "Finlande": 33.92,
    "Norvège": 33.92,
    "Suède": 33.92,
    "Italie": 33.92,
}

# ------------------------------------------------------------------
# Utils
# ------------------------------------------------------------------
@st.cache_data
def load_tariff() -> pd.DataFrame:
    if not TARIF_PATH.exists():
        st.error(f"Grille introuvable : {TARIF_PATH}")
        st.stop()
    return pd.read_excel(TARIF_PATH, sheet_name=0)


def arrondi_dizaine_sup(val: float) -> int:
    return int(math.ceil(val / 10) * 10)


def find_tariff(df: pd.DataFrame, pays: str, zone: str, poids: int):
    """Retourne (tarif €/100kg, libellé_colonne, borne_inf, borne_sup) ou None."""
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
                low, high = map(float, c.split(" kg")[0].split("-"))
                cols.append((high, low, c))
            except ValueError:
                continue
    cols.sort(key=lambda x: x[0])  # ordre bornes hautes croissant

    for high, low, col in cols:
        if poids <= high:
            return row[col], col, int(low), int(high)
    return None

# ------------------------------------------------------------------
# APP
# ------------------------------------------------------------------

def main():
    st.title("📦 Coûts export – Saisie palettes (HT)")

    df_tar = load_tariff()
    pays_liste = sorted(df_tar["Pays"].dropna().unique())

    with st.form("form"):
        col1, col2 = st.columns(2)
        with col1:
            pays = st.selectbox("Pays", pays_liste, index=pays_liste.index("France") if "France" in pays_liste else 0)
            zones = sorted(df_tar.loc[df_tar["Pays"].str.contains(pays, case=False, na=False), "Zone"].astype(str).unique())
            zone = st.selectbox("Zone (CP / code zone)", zones)
        with col2:
            opt_dg = st.checkbox("Produits dangereux")
            opt_rdv = st.checkbox("RDV tél. (manuel)")
            st.markdown(f"Surcharge carburant fixe : **{FUEL_PCT:.1f}%**")

        st.markdown("### Palettes (cm / kg)")
        default_df = pd.DataFrame({"Long(cm)": [80], "Larg(cm)": [120], "Haut(cm)": [100], "Poids(kg)": [100]})
        palettes = st.data_editor(default_df, num_rows="dynamic", use_container_width=True, key="palettes")
        submitted = st.form_submit_button("💰 Calculer")

    if not submitted:
        return

    palettes = palettes.dropna(how="all")
    if palettes.empty:
        st.error("Merci de saisir au moins une palette.")
        return
    try:
        pal = palettes.astype(float)
    except ValueError:
        st.error("Toutes les valeurs doivent être numériques.")
        return

    vol_m3 = (pal["Long(cm)"] / 100) * (pal["Larg(cm)"] / 100) * (pal["Haut(cm)"] / 100)
    poids_vol = vol_m3 * VOL_FACTOR
    total_reel = pal["Poids(kg)"].sum()
    total_vol = poids_vol.sum()

    poids_taxable = max(total_reel, total_vol)
    poids_arr = arrondi_dizaine_sup(poids_taxable)

    res_tarif = find_tariff(df_tar, pays, zone, poids_arr)
    if res_tarif is None:
        st.error("Tarif introuvable pour cette destination / zone.")
        return
    tarif, col_label, borne_inf, borne_sup = res_tarif

    fret_ht = (poids_arr / 100) * tarif
    fuel_ht = fret_ht * FUEL_PCT / 100

    frais = FIXED_FEES.copy()

    if opt_dg:
        md = OPTIONAL_FEES_BASE["Produits dangereux (base)"]
        for k, extra in DG_EXTRA.items():
            if pays.lower().startswith(k.lower()):
                md += extra
                break
        frais["Produits dangereux"] = md
    if opt_rdv:
        frais["RDV tél. manuel"] = OPTIONAL_FEES_BASE["RDV tél. (manuel)"]

    total_frais = sum(frais.values())
    sous_total_ht = fret_ht + fuel_ht + total_frais
    if sous_total_ht < MIN_PERCEPTION:
        frais["Minimum 75 €"] = MIN_PERCEPTION - sous_total_ht
        total_frais = sum(frais.values())
        sous_total_ht = fret_ht + fuel_ht + total_frais
    total_ht = sous_total_ht

    # ---------------- Affichage ----------------
    st.header("Résultat – Coûts export (HT)")

    # Méthode rappel
    st.markdown(
        """**Méthode “Coûts export”** &nbsp;: Poids taxable = max(poids réel, volume×250) → dizaine sup.  
        Coût = (poids/100 × tarif) + 10 % fuel + frais fixes + options → min 75 € HT."""
    )

    # ---- Tableau Paramètres ----
    parametres = {
        "Palettes": " • ".join(
            f"{l:.0f}×{w:.0f}×{h:.0f} / {p:.0f} kg"
            for l, w, h, p in pal[["Long(cm)", "Larg(cm)", "Haut(cm)", "Poids(kg)"].values]
        ),
        "Pays / zone": f"{pays} – {zone}",
        "Options": "  •  ".join([*("✔ Produits dangereux" if opt_dg else "",), *("✔ RDV tél. manuel" if opt_rdv else "",)]).strip("  •  ") or "—",
        "Poids réel total": f"{total_reel:.0f} kg",
        "Volume total": f"{total_vol:.4f} m³ × {VOL_FACTOR} = {total_vol*VOL_FACTOR:.0f} kg",
        "Poids taxable": f"max({total_reel:.0f} ; {total_vol*VOL_FACTOR:.0f}) → {poids_taxable:.0f} kg → arrondi → {poids_arr} kg",
        "Tarif appliqué": f"Tranche {borne_inf}-{borne_sup} kg – {tarif:,.2f} €/100 kg",
    }
    st.table(pd.Series(parametres, name="Valeur"))

    # ---- Tableau coûts ----
    lignes = [
        ("Fret", fret_ht),
        (f"Surcharge fuel {FUEL_PCT:.0f}%", fuel_ht),
    ]
    for lib, val in frais.items():
        lignes.append((lib, val))

    sous_tot = sum(v for _, v in lignes)
    lignes.append(("Sous-total", sous_tot))
    lignes.append(("TOTAL HT", total
