import streamlit as st
import sqlite3
import os
from datetime import datetime

# -----------------------------
# DATABASE SETUP
# -----------------------------
DB_PATH = "meldingen.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS meldingen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            naam TEXT,
            locatie TEXT,
            omschrijving TEXT,
            type TEXT,
            categorie TEXT,
            prioriteit TEXT,
            fotopad TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -----------------------------
# SAVE FUNCTION
# -----------------------------
def save_melding(naam, locatie, omschrijving, type_melding, categorie, prioriteit, fotopad):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO meldingen 
        (timestamp, naam, locatie, omschrijving, type, categorie, prioriteit, fotopad, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        naam, locatie, omschrijving, type_melding, categorie, prioriteit, fotopad, "Open"
    ))
    conn.commit()
    conn.close()

# -----------------------------
# DASHBOARD DATA
# -----------------------------
def load_meldingen():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM meldingen ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# -----------------------------
# STREAMLIT APP UI
# -----------------------------
st.set_page_config(page_title="Zorgpunt Risico Meldingen", layout="wide")

menu = ["Nieuwe melding", "Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

# ========================================
# PAGINA 1 — RISICOMELDING INDIENEN
# ========================================
if choice == "Nieuwe melding":

    st.title("Melding risico / gevaar / gebrek")

    st.info("""
    Via dit formulier kan u **risico’s, gevaren of gebreken** melden die u vaststelt in de opvang.
    Deze meldingen maken deel uit van de **officiële risicoanalyse**.
    Vul steeds uw **naam** en **opvanglocatie** in.
    """)

    naam = st.text_input("Naam medewerker *")
    locatie = st.selectbox("Opvanglocatie *", ["Babydroom", "’t Kinderhof", "Droomkind", "Droomhuis"])
    omschrijving = st.text_area("Omschrijving van het risico / gevaar / gebrek *", height=150)

    type_melding = st.selectbox("Type melding", ["Risico", "Gevaar", "Gebrek"])

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

    foto = st.file_uploader("Upload optionele foto")
    fotopad = ""

    if foto:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        fotopad = os.path.join("uploads", foto.name)
        with open(fotopad, "wb") as f:
            f.write(foto.getbuffer())

    if st.button("Melding verzenden"):

        if naam.strip() == "" or omschrijving.strip() == "":
            st.error("Gelieve naam en omschrijving verplicht in te vullen.")
        else:
            save_melding(naam, locatie, omschrijving, type_melding, categorie, prioriteit, fotopad)
            st.success("Melding succesvol opgeslagen!")
            st.balloons()


# ========================================
# PAGINA 2 — DASHBOARD
# ========================================
else:
    st.title("Dashboard risico meldingen")

    rows = load_meldingen()

    if not rows:
        st.warning("Nog geen meldingen geregistreerd.")
    else:
        # Tabel tonen
        kolommen = [
            "ID", "Tijdstip", "Naam", "Locatie", "Omschrijving",
            "Type", "Categorie", "Prioriteit", "Foto", "Status"
        ]

        df_data = []
        for r in rows:
            df_data.append(list(r))

        st.dataframe(df_data, use_container_width=True)

        st.subheader("Overzicht per prioriteit")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT 
                SUM(CASE WHEN prioriteit LIKE '1%' THEN 1 ELSE 0 END),
                SUM(CASE WHEN prioriteit LIKE '2%' THEN 1 ELSE 0 END),
                SUM(CASE WHEN prioriteit LIKE '3%' THEN 1 ELSE 0 END)
            FROM meldingen
        """)
        p1, p2, p3 = c.fetchone()
        conn.close()

        st.metric("Prioriteit 1 – Direct oplossen", p1 or 0)
        st.metric("Prioriteit 2 – Binnen de week", p2 or 0)
        st.metric("Prioriteit 3 – Binnen de maand", p3 or 0)

        st.success("Dashboard geladen.")
