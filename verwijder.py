import streamlit as st
import pandas as pd
import os

# --- CONFIGURATIE ---
DATA_FILE = "verlofregistratie_2025.csv"
BEHEERDERS_WACHTWOORD = "geheim123"  # <-- Vervang dit door jouw echte wachtwoord

st.set_page_config(page_title="Verwijder Verlofboeking", layout="wide")
st.title("❌ Verwijder Verlofboeking")

# --- BESTAAND CSV-BESTAND CONTROLEREN / AANMAKEN ---
if not os.path.exists(DATA_FILE):
    st.warning("⚠️ Geen verlofdata gevonden. Er wordt een leeg bestand aangemaakt.")
    pd.DataFrame(columns=["Naam", "Datum", "Tijdstip aanvraag"]).to_csv(DATA_FILE, index=False)

# --- AUTHENTICATIE ---
st.subheader("🔐 Beheerderslogin")
wachtwoord = st.text_input("Voer het beheerderswachtwoord in:", type="password")

if wachtwoord != BEHEERDERS_WACHTWOORD:
    if wachtwoord:
        st.error("❌ Ongeldig wachtwoord.")
    st.stop()

# --- LADEN DATA ---
verlof_data = pd.read_csv(DATA_FILE)
if verlof_data.empty:
    st.info("Er zijn momenteel geen verlofboekingen geregistreerd.")
    st.stop()

# --- SELECTIE VOOR VERWIJDERING ---
st.subheader("📋 Verwijder bestaande boeking")

naam_lijst = sorted(verlof_data["Naam"].unique())
geselecteerde_naam = st.selectbox("👤 Kies een naam", naam_lijst)

# Filter datums van deze persoon
datums_persoon = verlof_data[verlof_data["Naam"] == geselecteerde_naam]["Datum"].unique()
if len(datums_persoon) == 0:
    st.info("Deze persoon heeft geen geregistreerde boekingen.")
    st.stop()

geselecteerde_datum = st.selectbox("📅 Kies een datum", sorted(datums_persoon))

# --- VERWIJDERKNOP ---
if st.button("❌ Bevestig verwijdering"):
    # Verwijderen op basis van combinatie
    mask = ~((verlof_data["Naam"] == geselecteerde_naam) & (verlof_data["Datum"] == geselecteerde_datum))
    nieuwe_data = verlof_data[mask]

    # Opslaan
    nieuwe_data.to_csv(DATA_FILE, index=False)
    st.success(f"✅ Boeking van {geselecteerde_naam} op {geselecteerde_datum} is verwijderd.")

    # Herladen
    st.rerun()

# --- OPTIONEEL: TABEL LATEN ZIEN ---
with st.expander("📄 Toon alle huidige boekingen"):
    st.dataframe(verlof_data.sort_values(by=["Datum", "Naam"]))

st.write("📁 Bestandslocatie:", os.getcwd())
st.write("📄 Bestaat het bestand?", os.path.exists(DATA_FILE))

# Toon inhoud
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    st.write("📊 Inhoud van het bestand:", df)
