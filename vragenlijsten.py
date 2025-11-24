import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import random
import string
import datetime
import io

st.set_page_config(page_title="Zorgpunt Vragenlijsten", layout="centered")

# -----------------------------------------------------------
# HULPFUNCTIES
# -----------------------------------------------------------

def generate_unique_code():
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    numbers = ''.join(random.choices(string.digits, k=5))
    return f"ZORG-{letters}-{numbers}"

def create_certificate_html(name):
    today = datetime.date.today().strftime("%d/%m/%Y")
    unique_code = generate_unique_code()

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 40px;
            }}
            .title {{
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .name {{
                font-size: 26px;
                margin: 20px 0;
                font-weight: bold;
            }}
            .text {{
                font-size: 18px;
                margin: 10px 0;
            }}
            .footer {{
                position: fixed;
                bottom: 20px;
                width: 100%;
                text-align: center;
                font-size: 14px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="title">Certificaat van Deelname</div>
        <div class="text">Dit certificaat wordt uitgereikt aan:</div>
        <div class="name">{name}</div>
        <div class="text">
            voor het succesvol afronden van alle pedagogische modules<br>
            van Zorgpunt Meetjesland.
        </div>
        <div class="text">Datum: {today}</div>
        <div class="text">Unieke verificatiecode: <b>{unique_code}</b></div>

        <div class="footer">Zorgpunt Meetjesland – Bevestiging van deelname</div>
    </body>
    </html>
    """

    return html


def show_mc_question(question, options, correct, explanation):
    st.write(question)
    choice = st.radio("Kies een antwoord:", options, key=question)

    if st.button("Controleer", key=question + "_check"):
        if choice == correct:
            st.success(f"Juist! ✔️\n\n{explanation}")
        else:
            st.error(f"Fout ✖️\nHet juiste antwoord is: **{correct}**\n\n{explanation}")

def show_open_question(question, model_answer):
    st.write(question)
    st.text_area("Jouw antwoord:", key=question)

    if st.button("Controleer", key=question + "_open_check"):
        st.info("📘 **Modelantwoord:**")
        st.write(model_answer)


# -----------------------------------------------------------
# PAGINA’S
# -----------------------------------------------------------

def home():
    st.title("🌱 Zorgpunt Meetjesland – Interactieve Vragenlijsten")
    st.write("Kies een module:")

    if st.button("➡️ Module 1: Emmi Pikler"):
        st.session_state.page = "pikler"

    if st.button("➡️ Module 2: Vragenlijst A – Kinderopvang Basis"):
        st.session_state.page = "vragenlijst_a"

    if st.button("➡️ Module 3: Vragenlijst B – Rollen & Procedures"):
        st.session_state.page = "vragenlijst_b"

    # CERTIFICAAT TONEN ALS ALLES AFGEWERKT IS
    if st.session_state.get("done_pikler") and st.session_state.get("done_a") and st.session_state.get("done_b"):
        st.success("🎉 Je hebt alle modules afgerond!")
        name = st.text_input("Vul je naam in voor het certificaat (verplicht):")

     if name:
        html = create_certificate_html(name)
        st.download_button("📄 Download certificaat (HTML)",data=html,file_name="certificaat_zorgpunt.html",mime="text/html")


def pikler():
    st.title("🌿 Emmi Pikler – Zorgpunt Meetjesland")

    show_mc_question(
        "1. Wat is het belangrijkste principe van de Emmi Pikler-visie?",
        ["A. Snel leren", "B. Begeleider stuurt alles", "C. Kind op eigen tempo", "D. Ouders bepalen plan"],
        "C. Kind op eigen tempo",
        "Pikler legt sterk de nadruk op autonomie."
    )

    show_mc_question(
        "2. Hoe draagt Zorgpunt bij aan een rustige sfeer?",
        ["A. Kinderliedjes", "B. Hout & tapijten", "C. Alles wegbergen", "D. Blauwe/geel kleuren"],
        "B. Hout & tapijten",
        "Warme natuurlijke materialen zorgen voor rust."
    )

    show_mc_question(
        "3. Welk materiaal wordt bewust gekozen?",
        ["A. Plastic", "B. Natuurlijke materialen", "C. Elektronisch", "D. Enkel hout"],
        "B. Natuurlijke materialen",
        "Loose parts stimuleren creativiteit."
    )

    show_mc_question(
        "4. Waarom maar één begeleide activiteit?",
        ["A. Te weinig personeel", "B. Kind kan het al", "C. Niet te veel", "D. Niet opleggen"],
        "D. Niet opleggen",
        "Te veel sturen belemmert ontwikkeling."
    )

    show_mc_question(
        "5. Hoe wordt zelfstandigheid bij eten bevorderd?",
        ["A. Vast uur", "B. Grote tafel", "C. Kleine tafels", "D. Begeleider reikt alles aan"],
        "C. Kleine tafels",
        "Kleine groepjes geven rust."
    )

    show_open_question(
        "6. Hoe stimuleert Zorgpunt zelfstandigheid?",
        "Door materiaal op kindhoogte te zetten, kinderen keuzes te laten maken en hen actief te betrekken."
    )

    if st.button("✔️ Module afronden"):
        st.session_state.done_pikler = True
        st.session_state.page = "home"

    if st.button("⬅️ Terug naar start"):
        st.session_state.page = "home"


def vragenlijst_a():
    st.title("🧸 Vragenlijst A – Kinderopvang Basiskennis")

    show_open_question(
        "1. Wat is welbevinden en betrokkenheid?",
        "Welbevinden = hoe goed het kind zich voelt; betrokkenheid = hoe diep het speelt."
    )

    show_open_question(
        "2. Wat is educatieve ondersteuning?",
        "Aansluiten bij noden van kinderen via observatie en interactie."
    )

    show_open_question(
        "3. Wat is jouw draagkracht?",
        "Draagkracht = mentale buffer; bij lage draagkracht steun vragen."
    )

    if st.button("✔️ Module afronden"):
        st.session_state.done_a = True
        st.session_state.page = "home"

    if st.button("⬅️ Terug naar start"):
        st.session_state.page = "home"


def vragenlijst_b():
    st.title("📘 Vragenlijst B – Rollen & Procedures")

    show_open_question(
        "1. Dagelijkse zorg – hoe doe jij dit?",
        "Rust, nabijheid en veilige zorg bieden."
    )

    show_open_question(
        "2. Ontwikkelingsstimulering?",
        "Aansluiten bij ontwikkelingsniveau via observaties."
    )

    show_open_question(
        "3. Oudercommunicatie?",
        "Warm, eerlijk, tijdig en respectvol."
    )

    if st.button("✔️ Module afronden"):
        st.session_state.done_b = True
        st.session_state.page = "home"

    if st.button("⬅️ Terug naar start"):
        st.session_state.page = "home"


# -----------------------------------------------------------
# NAVIGATIE
# -----------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home()
elif st.session_state.page == "pikler":
    pikler()
elif st.session_state.page == "vragenlijst_a":
    vragenlijst_a()
elif st.session_state.page == "vragenlijst_b":
    vragenlijst_b()



