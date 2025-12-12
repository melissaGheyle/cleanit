import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

# -----------------------------
# GOOGLE SHEETS SETUP
# -----------------------------

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp"],
    scopes=SCOPE
)

client = gspread.authorize(creds)

SHEET_ID = "14zLgDSbj_bjuaPfLCyPg_7jJOVY_vfHHvpPsSzkSGZQ"
sheet = client.open_by_key(SHEET_ID).sheet1

# -----------------------------
# UPLOAD FOLDER
# -----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# E-MAIL INSTELLINGEN
# -----------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "melissagheyle@gmail.com"
SMTP_PASS = "skay tvei plvo lkql"   # Gmail App Password

MAIL_ONTVANGERS = [
    "melissagheyle@gmail.com",
    "joris_asseloos@hotmail.com"
]

def stuur_mail(naam, locatie, type_melding, categorie, prioriteit, omschrijving):
    onderwerp = "Nieuwe risico melding binnen Zorgpunt"
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


# -----------------------------
# GOOGLE SHEET FUNCTIONS
# -----------------------------

def save_melding(naam, locatie, omschrijving, type_melding, categorie, prioriteit, fotopad):
    try:
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            naam,
            locatie,
            omschrijving,
            type_melding,
            categorie,
            prioriteit,
            fotopad,
            "Open"
        ]
        sheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Kon melding niet opslaan in Google Sheets: {e}")
        return False


def load_meldingen():
    rows = sheet.get_all_values()
    return rows[1:]  # Skip header


def update_status(row_index, nieuwe_status):
    # row_index is 1-based (sheet), but our app displays 0-based
    sheet.update_cell(row_index + 1, 9, nieuwe_status)  # kolom 9 = status


# -----------------------------
# STREAMLIT INTERFACE
# -----------------------------

st.set_page_config(page_title="Zorgpunt Risico Meldingen", layout="wide")

menu = ["Nieuwe melding", "Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# PAGINA: Nieuwe melding
# -----------------------------
if choice == "Nieuwe melding":

    st.title("Risico / Gevaar / Gebrek melden")

    naam = st.text_input("Naam medewerker *")
    locatie = st.selectbox("Opvanglocatie *", ["Babydroom", "’t Kinderhof", "Droomkind", "Droomhuis"])
    omschrijving = st.text_area("Omschrijving *", height=150)

    type_melding = st.selectbox("Type melding", ["Risico", "Gevaar", "Gebrek"])

    categorie = st.selectbox("Categorie", [
        "Toezicht en handelingen", "Toegang", "Binnenruimtes", "Binnenklimaat",
        "Buitenspelen", "Vervoer", "Slapen", "Verzorging", "Hygiëne",
        "Vaccinaties", "Zieke kinderen en koorts", "Geneesmiddelen"
    ])

    prioriteit = st.selectbox("Prioriteit", [
        "1 – Direct oplossen",
        "2 – Binnen de week",
        "3 – Binnen de maand"
    ])

    foto = st.file_uploader("Upload optionele foto")
    fotopad = ""

    if foto:
        save_path = os.path.join(UPLOAD_FOLDER, foto.name)
        with open(save_path, "wb") as f:
            f.write(foto.getbuffer())
        fotopad = save_path

    if st.button("Melding verzenden"):
        if not naam or not omschrijving:
            st.error("Naam en omschrijving zijn verplicht.")
        else:
            if save_melding(naam, locatie, omschrijving, type_melding, categorie, prioriteit, fotopad):
                stuur_mail(naam, locatie, type_melding, categorie, prioriteit, omschrijving)
                st.success("Melding succesvol opgeslaan!")
                st.balloons()

# -----------------------------
# PAGINA: Dashboard
# -----------------------------
else:
    st.title("Dashboard risico meldingen")

    rows = load_meldingen()

    if not rows:
        st.warning("Nog geen meldingen.")
    else:
        st.dataframe(rows, use_container_width=True)

        # Prioriteitentelling
        p1 = sum(1 for r in rows if r[6].startswith("1"))
        p2 = sum(1 for r in rows if r[6].startswith("2"))
        p3 = sum(1 for r in rows if r[6].startswith("3"))

        st.subheader("Prioriteiten")
        st.metric("1 – Direct oplossen", p1)
        st.metric("2 – Binnen de week", p2)
        st.metric("3 – Binnen de maand", p3)

        # STATUS AANPASSEN
        st.subheader("Status aanpassen")

        indices = list(range(len(rows)))
        melding_nummer = st.selectbox("Kies melding (rij-index)", indices)

        nieuwe_status = st.selectbox("Nieuwe status", ["Open", "In behandeling", "Opgelost"])

        if st.button("Status bijwerken"):
            update_status(melding_nummer, nieuwe_status)
            st.success("Status bijgewerkt! Herlaad de pagina om het te zien.")
