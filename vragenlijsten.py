import streamlit as st
import datetime
import random
import string

st.set_page_config(page_title="Zorgpunt Vragenlijsten", layout="centered")

# =============================================================
# HULPFUNCTIES
# =============================================================

def unique_code():
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    numbers = ''.join(random.choices(string.digits, k=5))
    return f"ZORG-{letters}-{numbers}"

def cert_html(name, score, max_score):
    today = datetime.date.today().strftime("%d/%m/%Y")
    perc = round(score / max_score * 100)

    status = "GESLAAGD" if perc >= 70 else "VOLTOOID (niet geslaagd)"

    html = f"""
    <html><body style="font-family:Arial; text-align:center; padding:40px;">
    <h1>Certificaat van Deelname</h1>
    <h3>Dit certificaat wordt uitgereikt aan:</h3>
    <h2>{name}</h2>
    <p>voor het succesvol afronden van alle pedagogische modules<br>
    van Zorgpunt Meetjesland.</p>

    <h3>Score: {score} / {max_score}  —  {perc}%</h3>
    <h2>{status}</h2>

    <p>Datum: {today}</p>
    <p>Unieke verificatiecode: <b>{unique_code()}</b></p>

    <br><br><hr>
    <p><i>Zorgpunt Meetjesland — Bevestiging van deelname</i></p>
    </body></html>
    """
    return html

def score_point_open(answer):
    return 1 if answer.strip() != "" else 0

# =============================================================
# VRAGEN (volledig uit PDF)
# =============================================================

# ------------------------
# MODULE 1 – Pikler (MC + open)
# ------------------------
pikler_questions = [
    # (vraag, opties, juiste, uitleg)
    ("Wat is het belangrijkste principe van de Emmi Pikler-visie?",
     ["A. Snel leren", "B. Begeleider stuurt alles", "C. Kind op eigen tempo", "D. Ouders bepalen plan"],
     "C. Kind op eigen tempo",
     "Pikler legt sterk de nadruk op autonomie en eigen initiatief."),

    ("Hoe draagt Zorgpunt bij aan een rustige sfeer?",
     ["A. Kinderliedjes", "B. Hout & tapijten", "C. Alles wegbergen", "D. Blauwe/geel kleuren"],
     "B. Hout & tapijten",
     "Warme natuurlijke materialen zorgen voor rust."),

    ("Welk materiaal wordt bewust gekozen?",
     ["A. Plastic speelgoed", "B. Natuurlijke materialen", "C. Elektronica", "D. Enkel hout"],
     "B. Natuurlijke materialen",
     "Loose parts en echte materialen stimuleren ontwikkeling."),

    ("Waarom maar één begeleide activiteit per thema?",
     ["A. Te weinig personeel", "B. Kind kan het al", "C. Niet te veel", "D. Niet opleggen"],
     "D. Niet opleggen",
     "Te veel sturen belemmert de natuurlijke ontwikkeling."),

    ("Hoe wordt zelfstandigheid bij eten bevorderd?",
     ["A. Vast uur", "B. Grote tafel", "C. Kleine tafels", "D. Begeleider reikt alles aan"],
     "C. Kleine tafels",
     "Kleine groepjes bevorderen rust en autonomie.")
]

pikler_open = [
    ("Hoe stimuleert Zorgpunt zelfstandigheid volgens Pikler?",
     "Door materiaal op kindhoogte te zetten, keuzes te bieden en kinderen actief te betrekken.")
]

# ------------------------
# MODULE 2 – Vragenlijst A
# ------------------------
vragenlijst_A = [
    ("Wat is welbevinden en betrokkenheid in de opvang? Wat doe je als deze laag is?",
     "Welbevinden = hoe gelukkig het kind is. Betrokkenheid = hoe geconcentreerd het speelt. Bij lage niveaus: meer nabijheid, rust en afstemming bieden."),
    ("Wat is educatieve ondersteuning? Hoe ben jij daar zelf in gevormd?",
     "Educatieve ondersteuning = aansluiten bij noden, stimuleren, observeren."),
    ("Wat is jouw draagkracht? Wat doe je als deze minder wordt?",
     "Draagkracht = mentale buffer. Bij overbelasting: steun vragen, grenzen bewaken."),
    ("Hoe zijn de leefgroepen ingedeeld? Wat is belangrijk voor iedere leefgroep?",
     "Leefgroepen volgens leeftijd en ontwikkeling. Baby's → verzorging; peuters → structuur en spel."),
    ("Hoe doe jij toezicht op de rustruimtes? Waarom doe je het zo?",
     "Regelmatig controleren, luisteren, rust bewaken."),
    ("Hoe bevorder je het contact met ouders? Zijn er hulpmiddelen?",
     "Warm contact, overdrachten, formulieren, open communicatie."),
    ("Welke risico’s zijn er in de opvang en is er een procedure?",
     "Valgevaar, ziekte, ontsnappen. Ja, vaste procedures."),
    ("Waar registreer jij je uren? Ken je de ratio van begeleiders?",
     "Via aanwezigheidsblad of digitaal. Ratio = begeleiders/kinderen verhouding.")
]

# ------------------------
# MODULE 3 – Vragenlijst B
# ------------------------
vragenlijst_B = [
    ("Dagelijkse zorg – hoe doe jij dit?",
     "Rust, nabijheid en veilige verzorging aanbieden."),
    ("Ontwikkelingsstimulering – hoe doe jij dit?",
     "Aansluiten bij ontwikkeling via observaties."),
    ("Oudercommunicatie – hoe doe jij dit?",
     "Warm, eerlijk en tijdig communiceren."),
    ("Een ouder heeft een klacht over voeding. Hoe ga je daarmee om?",
     "Luisteren, erkennen, melden aan verantwoordelijke, procedure volgen."),
    ("Hebben wij een procedure bij klachten? Wat zijn de stappen?",
     "1) Ontvangst klacht  2) Onderzoek  3) Communicatie naar ouders."),
    ("Wat is grensoverschrijdend gedrag? Geef 2 voorbeelden.",
     "Fysiek geweld, verbaal geweld, negeren, vernederen."),
    ("Crisisprocedures: welke stappen neem je als begeleider?",
     "A) Alarmeren  B) Hulpdiensten  C) Veiligheid garanderen."),
    ("Hoe zijn de leefgroepen ingedeeld? Wat is belangrijk?",
     "Baby's → verzorging; peuters → structuur, taal en zelfstandigheid."),
    ("Hoe doe je toezicht op de rustruimtes? Waarom?",
     "Regelmatige fysieke controle elke 10–15 min, aandacht voor welzijn."),
    ("Welke risico’s zijn er in de opvang en is er een procedure?",
     "Ja, risico-analyse in rode map, jaarlijks onderhoud."),
]

# =============================================================
# SESSIESTATE
# =============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "score" not in st.session_state:
    st.session_state.score = 0

if "max_score" not in st.session_state:
    st.session_state.max_score = (
        len(pikler_questions) + len(pikler_open) +
        len(vragenlijst_A) +
        len(vragenlijst_B)
    )

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "module" not in st.session_state:
    st.session_state.module = None

# =============================================================
# NAVIGATIE
# =============================================================

def go_home():
    st.session_state.page = "home"
    st.session_state.q_index = 0
    st.session_state.module = None

# =============================================================
# MODULE ENGINE (UNIVERSEEL)
# =============================================================

def run_module(title, qlist, is_mc=False):
    idx = st.session_state.q_index

    st.title(title)

    # EINDE MODULE
    if idx >= len(qlist):
        st.success("Module afgerond!")
        st.button("Terug naar start", on_click=go_home)
        return

    # ---------------------------------------------
    # MEERKEUZE
    # ---------------------------------------------
    if is_mc:
        vraag, opties, juist, uitleg = qlist[idx]
        st.write(vraag)
        keuze = st.radio("Kies:", opties)

        if st.button("Controleer"):
            if keuze == juist:
                st.success("Juist!")
                st.session_state.score += 1
            else:
                st.error(f"Fout. Juiste antwoord: **{juist}**")
            st.info(uitleg)

            st.session_state.q_index += 1
            st.experimental_rerun()

    # ---------------------------------------------
    # OPEN VRAAG
    # ---------------------------------------------
    else:
        vraag, model = qlist[idx]
        st.write(vraag)
        ans = st.text_area("Jouw antwoord:")

        if st.button("Controleer"):
            if ans.strip() != "":
                st.session_state.score += 1

            st.info("Modelantwoord:")
            st.write(model)

            st.session_state.q_index += 1
            st.experimental_rerun()


# =============================================================
# HOME
# =============================================================

if st.session_state.page == "home":
    st.title("🌱 Zorgpunt Meetjesland – Interactieve Vragenlijsten")

    st.write("Kies een module:")

    if st.button("➡️ Module 1: Emmi Pikler"):
        st.session_state.page = "m1"
        st.session_state.module = "m1"
        st.session_state.q_index = 0

    if st.button("➡️ Module 2: Vragenlijst A"):
        st.session_state.page = "m2"
        st.session_state.module = "m2"
        st.session_state.q_index = 0

    if st.button("➡️ Module 3: Vragenlijst B"):
        st.session_state.page = "m3"
        st.session_state.module = "m3"
        st.session_state.q_index = 0

    # CERTIFICAAT ALS 3 MODULES GEDAAN zijn (score > 0)
    if st.session_state.score > 0:
        st.subheader("📜 Certificaat genereren")

        name = st.text_input("Naam:")

        if name:
            html = cert_html(name, st.session_state.score, st.session_state.max_score)
            st.download_button(
                "📄 Download certificaat (HTML)",
                data=html,
                file_name="certificaat_zorgpunt.html",
                mime="text/html"
            )

# =============================================================
# MODULE RUNNERS
# =============================================================

elif st.session_state.page == "m1":
    run_module("Module 1 – Emmi Pikler", pikler_questions, is_mc=True)
    if st.session_state.q_index >= len(pikler_questions):
        run_module("Module 1 – Emmi Pikler (Open Vraag)", pikler_open)

elif st.session_state.page == "m2":
    run_module("Module 2 – Vragenlijst A", vragenlijst_A)

elif st.session_state.page == "m3":
    run_module("Module 3 – Vragenlijst B", vragenlijst_B)
