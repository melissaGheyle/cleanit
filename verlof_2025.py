import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Verlofplanner 2025", layout="wide")
st.title("📅 Verlofplanner 2025")

DATA_FILE = "verlofregistratie_2025.csv"

# 📂 Stap 1: laad of initialiseer databestand
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["Naam", "Datum", "Tijdstip aanvraag"]).to_csv(DATA_FILE, index=False)

# 👤 Stap 2: naam en datum invoer
naam = st.text_input("👤 Jouw naam")
kies_datum = st.date_input("📆 Kies een verlofdag", value=datetime.date(2025, 1, 1),
                            min_value=datetime.date(2025, 1, 1), max_value=datetime.date(2025, 12, 31))

kies_datum_str = kies_datum.strftime('%d-%m-%Y')
verlof_data = pd.read_csv(DATA_FILE, dtype={"Datum": str})
reeds_afwezig = verlof_data[verlof_data["Datum"] == kies_datum_str]

# 🔎 Feedback over beschikbaarheid op gekozen datum
if not naam.strip():
    st.warning("Vul je naam in om verder te gaan.")
else:
    if not reeds_afwezig.empty:
        afwezige = reeds_afwezig.iloc[0]["Naam"]
        st.warning(f"⚠️ Opgelet: {afwezige} heeft al verlof op deze dag.")
    else:
        st.info("✅ Deze dag is momenteel vrij.")

# Invoer afhandelen
if naam.strip() and st.button("📅 Verlof aanvragen"):
    if not reeds_afwezig.empty:
        afwezige = reeds_afwezig.iloc[0]["Naam"]
        st.error(f"❌ Niet mogelijk: {afwezige} heeft al verlof op {kies_datum_str}.")
    else:
        tijdstip_aanvraag = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        nieuwe_invoer = pd.DataFrame({
            "Naam": [naam.strip()],
            "Datum": [kies_datum_str],
            "Tijdstip aanvraag": [tijdstip_aanvraag]
        })
        verlof_data = pd.concat([verlof_data, nieuwe_invoer], ignore_index=True)
        verlof_data.to_csv(DATA_FILE, index=False)
        st.success(f"✅ Verlof geboekt op {kies_datum_str} voor {naam.strip()}.")

# 🔘 Download-link voor het volledige bestand
if st.button("📥 Download overzicht als CSV-bestand"):
    with open(DATA_FILE, "rb") as f:
        st.download_button(label="📄 Download verlofregistratie_2025.csv",
                           data=f,
                           file_name="verlofregistratie_2025.csv",
                           mime="text/csv")
