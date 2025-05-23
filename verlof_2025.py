import streamlit as st
import pandas as pd
import datetime
import os

# Pagina-instelling
st.set_page_config(page_title="Verlofplanner 2025", layout="wide")
st.title("📅 Verlofplanner 2025")

DATA_FILE = "verlofregistratie_2025.csv"
GOOGLE_DRIVE_CSV_URL = "https://drive.google.com/uc?export=download&id=1H2AoP_MGa3m_nIfxEaBdJewfrEMZ0CxG"

# Capaciteit per dag
capaciteit_per_dag = {
    '1/07/2025': 3, '2/07/2025': 2, '3/07/2025': 3, '4/07/2025': 2,
    '7/07/2025': 3, '8/07/2025': 4, '9/07/2025': 4, '10/07/2025': 2,
    '11/07/2025': 1, '14/07/2025': 2, '15/07/2025': 2, '16/07/2025': 3,
    '17/07/2025': 3, '18/07/2025': 3, '28/07/2025': 1, '29/07/2025': 1,
    '30/07/2025': 1, '31/07/2025': 0, '1/08/2025': 1, '4/08/2025': 0,
    '5/08/2025': 0, '6/08/2025': 0, '7/08/2025': 1, '8/08/2025': 0,
    '11/08/2025': 0, '12/08/2025': 0, '13/08/2025': 0, '14/08/2025': 1,
    '18/08/2025': 0, '19/08/2025': 0, '20/08/2025': 0, '21/08/2025': 0,
    '22/08/2025': 2, '25/08/2025': 0, '26/08/2025': 0, '27/08/2025': 0,
    '28/08/2025': 0, '29/08/2025': 1
}

# Laad bestand indien niet lokaal
if not os.path.exists(DATA_FILE):
    try:
        df = pd.read_csv(GOOGLE_DRIVE_CSV_URL)
        df.to_csv(DATA_FILE, index=False)
        st.info("📂 CSV-bestand is ingeladen vanaf Google Drive.")
    except Exception as e:
        st.error("❌ Kan CSV-bestand niet ophalen van Google Drive.")
        df = pd.DataFrame(columns=["Naam", "Datum", "Tijdstip aanvraag"])
        df.to_csv(DATA_FILE, index=False)

# Lees lokale data
verlof_data = pd.read_csv(DATA_FILE, dtype={"Datum": str})

# Tijdstipfilter instellen (alleen boekingen vanaf 1 juni tellen mee)
filter_moment = datetime.datetime(2025, 6, 1, 0, 0, 0)

# Stap 1: veilige omzetting naar datetime
verlof_data["Tijdstip aanvraag"] = pd.to_datetime(
    verlof_data["Tijdstip aanvraag"],
    format='%d-%m-%Y %H:%M:%S',
    errors='coerce'
)

# Stap 2: detectie foutieve tijdstempels
ongeldige_rijen = verlof_data[verlof_data["Tijdstip aanvraag"].isna()]
if not ongeldige_rijen.empty:
    st.warning("⚠️ Er zijn boekingen met ongeldige of ontbrekende tijdstempels (worden genegeerd):")
    st.dataframe(ongeldige_rijen)

# Stap 3: filter op geldige, recente aanvragen
verlof_data_geldig = verlof_data[
    (verlof_data["Tijdstip aanvraag"].notna()) &
    (verlof_data["Tijdstip aanvraag"] >= filter_moment)
]

# Invoer
naam = st.text_input("👤 Jouw naam").strip().capitalize()
kies_datum = st.date_input("📆 Kies een verlofdag", value=datetime.date(2025, 1, 1),
                           min_value=datetime.date(2025, 1, 1), max_value=datetime.date(2025, 12, 31))
kies_datum_str = kies_datum.strftime('%-d/%m/%Y')  # bv. 1/07/2025

# Beschikbaarheidscontrole (enkel geldige boekingen)
reeds_afwezig = verlof_data_geldig[verlof_data_geldig["Datum"] == kies_datum_str]
aantal_huidige_boekingen = len(reeds_afwezig)
max_toegelaten = capaciteit_per_dag.get(kies_datum_str, 1)

st.markdown("📌 <small>Enkel aanvragen vanaf 1 juni 2025 worden meegeteld voor beschikbaarheid.</small>", unsafe_allow_html=True)

# Feedback
if not naam:
    st.warning("Vul je naam in om verder te gaan.")
else:
    if aantal_huidige_boekingen >= max_toegelaten:
        st.error(f"❌ Deze dag ({kies_datum_str}) is volzet ({aantal_huidige_boekingen}/{max_toegelaten}).")
    else:
        over = max_toegelaten - aantal_huidige_boekingen
        st.success(f"✅ Deze dag is beschikbaar ({over} plaats(en) over).")

# Verlof aanvragen
if naam and st.button("📅 Verlof aanvragen"):
    dubbele_boeking = (verlof_data["Datum"] == kies_datum_str) & (verlof_data["Naam"] == naam)

    if dubbele_boeking.any():
        st.error(f"❌ Je hebt al verlof geboekt op {kies_datum_str}.")
    elif aantal_huidige_boekingen >= max_toegelaten:
        st.error(f"❌ Kan niet boeken. Maximum aantal personen ({max_toegelaten}) is al bereikt.")
    else:
        tijdstip_aanvraag = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        nieuwe_invoer = pd.DataFrame({
            "Naam": [naam],
            "Datum": [kies_datum_str],
            "Tijdstip aanvraag": [tijdstip_aanvraag]
        })
        verlof_data = pd.concat([verlof_data, nieuwe_invoer], ignore_index=True)
        verlof_data.to_csv(DATA_FILE, index=False)
        st.success(f"✅ Verlof geboekt op {kies_datum_str} voor {naam}.")

# Downloadknop
st.markdown("### 📤 Download verlofoverzicht")
with open(DATA_FILE, "rb") as f:
    st.download_button(label="📄 Download verlofregistratie_2025.csv",
                       data=f,
                       file_name="verlofregistratie_2025.csv",
                       mime="text/csv")
