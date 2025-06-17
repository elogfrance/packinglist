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
    "Dédouanement export": 35,
    "Frais de dossier": 15,
}

def main():
    st.title("🚚 Estimation des coûts transport export")

    # Formulaire de saisie
    with st.form("formulaire"):        
        col1, col2 = st.columns(2)
        with col1:
            pays = st.selectbox("🌍 Pays de destination", ["Algérie", "Maroc", "Tunisie"], index=0)
            devis_monnaie = st.selectbox("💱 Monnaie de devis", ["EUR", "USD"], index=0)
            nb_colis = st.number_input("📦 Nombre de colis", min_value=1, value=1)
        with col2:
            pal_file = st.file_uploader("📁 Détail des colis (Excel)", type=["xlsx"])
            submit = st.form_submit_button("📊 Calculer les coûts")

    if submit:
        if not pal_file:
            st.error("❌ Merci d'importer un fichier contenant les dimensions des colis.")
            return

        try:
            pal = pd.read_excel(pal_file)
            required_cols = ["Long(cm)", "Larg(cm)", "Haut(cm)", "Poids(kg)"]
            if not all(col in pal.columns for col in required_cols):
                st.error("❌ Le fichier doit contenir les colonnes : Long(cm), Larg(cm), Haut(cm), Poids(kg).")
                return

            total_volume = 0
            total_weight = 0

            for l, w, h, p in pal[["Long(cm)", "Larg(cm)", "Haut(cm)", "Poids(kg)"]].values:
                if pd.isna(l) or pd.isna(w) or pd.isna(h) or pd.isna(p):
                    continue
                try:
                    vol = (float(l) * float(w) * float(h)) / 1_000_000  # volume en m³
                    total_volume += vol
                    total_weight += float(p)
                except ValueError:
                    continue

            vol_weight = total_volume * VOL_FACTOR
            taxable_weight = max(total_weight, vol_weight)

            # Récupérer tarif selon pays et tranche de poids
            df_tarif = pd.read_excel(TARIF_PATH, sheet_name=pays)
            tranche = df_tarif[df_tarif["Poids max"] >= taxable_weight].iloc[0]
            base_cost = tranche["Tarif"]

            fuel_surcharge = base_cost * (FUEL_PCT / 100)
            total_fees = sum(FIXED_FEES.values())
            total = base_cost + fuel_surcharge + total_fees
            total = max(total, MIN_PERCEPTION)

            st.success("✅ Estimation complétée :")
            st.markdown(f"**Poids réel total :** {total_weight:.2f} kg")
            st.markdown(f"**Poids volumétrique :** {vol_weight:.2f} kg")
            st.markdown(f"**Poids taxable :** {taxable_weight:.2f} kg")
            st.markdown(f"**Tarif de base :** {base_cost:.2f} €")
            st.markdown(f"**Surcharge carburant ({FUEL_PCT:.0f}%) :** {fuel_surcharge:.2f} €")
            st.markdown(f"**Frais fixes :** {total_fees:.2f} €")
            st.markdown(f"### 💰 Total estimé : {total:.2f} € HT")

        except Exception as e:
            st.error(f"❌ Erreur lors du traitement : {e}")
