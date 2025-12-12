import streamlit as st
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import gspread
from google.oauth2.service_account import Credentials


# ============================================
# GOOGLE SHEETS VERBINDING
# ============================================

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp"],
    scopes=SCOPE
)

client = gspread.authorize(creds)

# NIEUWE SHEET ID
SHEET_ID = "1k03IUszL8tp_RrSx3NBuZpBLdiM-MZugTKeeNgUzYqc"
sheet = client.open_by_key(SHEET_ID).sheet1


# ============================================
# SMTP INSTELLINGEN
# ============================================

SMTP_USER = st.secrets["smtp"]["user"]
SMTP_PASS = st.secrets["smtp"]["password"]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

MAIL_ONTVANGERS = [
    "melissagheyle@gmail.com",
    "joris_asseloos@hotmail.com",
    "medewerkers.kinderopvang@gmail.com",
    "zorgpuntmeetjesland@gmail.com"
]


def stuur_mail(naam, locatie, type_melding, categorie, prioriteit, omschrijving):
    onderwerp = "Nieuwe risico melding - Zorgpunt"

    html = f"""
    <h3>Nieuwe risico melding</h3>
    <p><b>Naam:</b> {naam}</p>
    <p><b>Locatie:</b> {locatie}</p>
    <p><b>Type:</b> {type_melding}</p>
    <p><b>Categorie:</b> {categorie}</p>
    <p><b>Prioriteit:</b> {prioriteit}</p>
    <p><b>Omschrijving:</b> {omschrijving}</p>
    """

    msg = MIMEText(html, "html")
    msg["Subject"] = onderwerp
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(MAIL_ONTVANGERS)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, MAIL_ONTVANGERS, msg.as_string())
    except Exception as e:
        st.error(f"Kon geen e-mail verzenden: {e}")


# ============================================
# FOTO-UPLOAD MAP
# ============================================

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================
# NIEUWE MELDING OPSLAAN IN GOOGLE SHEET
# ============================================

def save_to_sheet(naam, locatie, omschrijving, type_melding, categorie, prioriteit, fotopad):
    new_row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        naam,
        locatie,
        omschrijving,
        type_melding,
        categorie,
        prioriteit,
        fotopad,
        "Open",
    ]

    sheet.append_row(new_row)


def load_sheet_data():
    return sheet.get_all_values()


def update_status(row_index, new_status):
    sheet.update_cell(row_index, 9, new_status)


# ============================================
# STREAMLIT INTERFACE
# ============================================

st.set_page_config(page_title="Zorgpunt Risico Meldingen", layout="wide")

menu = ["Nieuwe melding", "Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)


# ==================================================
# PAGINA 1 – MELDING AANMAKEN
# ==================================================
if choice == "Nieuwe melding":

    st.title("Risico / Gevaar / Gebrek melden")

    naam = st.text_input("Naam medewerker *")
    locatie = st.selectbox("Opvanglocatie *", ["Babydroom", "’t Kinderhof", "Droomkind", "Droomhuis"])
    omschrijving = st.text_area("Omschrijving *")

    type_melding = st.selectbox("Type", ["Risico", "Gevaar", "Gebrek"])

    categorie = st.selectbox("Categorie", [
        "Toezicht en handelingen",
        "Toegang",
        "Binnenruimtes",
        "Binnenklimaat",
        "Buitenspelen",
        "Vervoer",
        "Slapen",
        "Verzorging",
        "Hygiëne",
        "Vaccinaties",
        "Zieke kinderen en koorts",
        "Geneesmiddelen"
    ])

    prioriteit = st.selectbox("Prioriteit", [
        "1 – Direct oplossen",
        "2 – Binnen de week",
        "3 – Binnen de maand"
    ])

    foto = st.file_uploader("Upload foto (optioneel)")
    fotopad = ""

    if foto:
        save_path = os.path.join(UPLOAD_FOLDER, foto.name)
        with open(save_path, "wb") as f:
            f.write(foto.getbuffer())
        fotopad = save_path

    if st.button("Melding indienen"):
        if not naam or not omschrijving:
            st.error("Naam en omschrijving zijn verplicht.")
        else:
            save_to_sheet(naam, locatie, omschrijving, type_melding, categorie, prioriteit, fotopad)
            stuur_mail(naam, locatie, type_melding, categorie, prioriteit, omschrijving)
            st.success("Melding opgeslagen!")
            st.balloons()


# ==================================================
# PAGINA 2 – DASHBOARD
# ==================================================
else:
    st.title("Dashboard Risico Meldingen")

    data = load_sheet_data()

    if len(data) <= 1:
        st.warning("Nog geen meldingen.")
    else:
        headers = [
            "Tijdstip", "Naam", "Locatie", "Omschrijving",
            "Type", "Categorie", "Prioriteit", "Foto", "Status"
        ]

        rows = data[1:]  # skip header row

        st.dataframe(rows, use_container_width=True)

        # Status wijzigen
        st.subheader("Status aanpassen")

        indices = list(range(2, len(rows) + 2))  # row numbers in sheet
        gekozen_index = st.selectbox("Kies rijnummer", indices)

        nieuwe_status = st.selectbox("Nieuwe status", ["Open", "In behandeling", "Opgelost"])

        if st.button("Status bijwerken"):
            update_status(gekozen_index, nieuwe_status)
            st.success("Status bijgewerkt! Herlaad de pagina.")



