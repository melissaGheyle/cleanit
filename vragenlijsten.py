import streamlit as st
import datetime
import random
import string

st.set_page_config(page_title="Zorgpunt Vragenlijsten", layout="centered")

# =============================================================
# HELPERS
# =============================================================

def generate_code():
    return "ZORG-" + "".join(random.choices(string.ascii_uppercase, k=4)) + "-" + "".join(random.choices(string.digits, k=5))

def cert_html(name, score, max_score):
    today = datetime.date.today().strftime("%d/%m/%Y")
    perc = round(score / max_score * 100)
    status = "GESLAAGD" if perc >= 70 else "VOLTOOID (niet geslaagd)"

    return f"""
    <html>
    <body style="font-family:Arial; text-align:center; padding:40px;">
        <h1>Certificaat van Deelname</h1>
        <h3>Uitgereikt aan:</h3>
        <h2>{name}</h2>

        <p>na het afronden van alle pedagogische modules<br>Zorgpunt Meetjesland</p>

        <h3>Score: {score} / {max_score} ({perc}%)</h3>
        <h2>{status}</h2>

        <p>Datum: {today}</p>
        <p>Unieke verificatiecode: <b>{generate_code()}</b></p>

        <br><hr><br>
        <p><i>Zorgpunt Meetjesland – Bevestiging van deelname</i></p>
    </body>
    </html>
    """

def store_feedback(msg_type, msg_main, explanation):
    st.session_state.last_fb = (msg_type, msg_main, explanation)

def show_feedback():
    if "last_fb" in st.session_state:
        t, msg, exp = st.session_state.last_fb
        if t == "success":
            st.success(msg)
        else:
            st.error(msg)
        st.info(exp)
        del st.session_state.last_fb


def point_if_filled(text):
    return 1 if text.strip() != "" else 0


# =============================================================
# VRAGEN UIT DE PDF'S
# =============================================================

# MODULE 1 – Pikler (MC)
pikler_mc = [
    ("Wat is het belangrijkste principe van de Emmi Pikler-visie?",
     ["A. Snel leren", "B. Begeleider stuurt", "C. Kind op eigen tempo", "D. Ouders bepalen"],
     "C. Kind op eigen tempo",
     "Pikler legt sterk de nadruk op autonomie."),
    ("Hoe draagt Zorgpunt bij aan een rustige sfeer?",
     ["A. Kinderliedjes", "B. Hout & tapijten", "C. Alles wegbergen", "D. Blauwe/geel kleuren"],
     "B. Hout & tapijten",
     "Warme natuurlijke materialen zorgen voor rust."),
    ("Welk materiaal wordt bewust gekozen?",
     ["A. Plastic", "B. Natuurlijke materialen", "C. Elektronica", "D. Enkel hout"],
     "B. Natuurlijke materialen",
     "Loose parts stimuleren creativiteit."),
    ("Waarom maar één begeleide activiteit per thema?",
     ["A. Te weinig personeel", "B. Kind kan het al", "C. Niet te veel", "D. Niet opleggen"],
     "D. Niet opleggen",
     "Te veel sturen belemmert ontwikkeling."),
    ("Hoe wordt zelfstandigheid bij eten bevorderd?",
     ["A. Vast uur", "B. Grote tafel", "C. Kleine tafels", "D. Begeleider reikt alles aan"],
     "C. Kleine tafels",
     "Kleine groepjes bevorderen rust.")
]

# MODULE 1 – Pikler OPEN
pikler_open = [
    ("Hoe stimuleert Zorgpunt zelfstandigheid?",
     "Door materiaal op kindhoogte te zetten, keuzes te bieden en kinderen actief te betrekken.")
]

# MODULE 2 – A
vragen_A = [
    ("Wat is welbevinden en betrokkenheid? Wat doe je als deze laag is?",
     "Welbevinden = hoe goed het kind zich voelt; betrokkenheid = hoe diep het speelt."),
    ("Wat is educatieve ondersteuning?",
     "Stimuleren, observeren, aansluiten bij noden."),
    ("Wat is jouw draagkracht? Wat doe je als die minder wordt?",
     "Steun zoeken, grenzen stellen."),
    ("Hoe zijn de leefgroepen ingedeeld?",
     "Baby's → verzorging; peuters → structuur."),
    ("Hoe doe jij toezicht op rustruimtes?",
     "Regelmatig controleren, rust bewaken."),
    ("Hoe bevorder je contact met ouders?",
     "Warme overdrachten, formulieren, open communicatie."),
    ("Welke risico’s zijn er in de opvang?",
     "Valgevaar, ziekte, ontsnappen. Procedure aanwezig."),
    ("Waar registreer jij je uren? Wat is ratio?",
     "Aanwezigheidsblad/digitaal. Ratio = begeleiders/kinderen.")
]

# MODULE 3 – B
vragen_B = [
    ("Dagelijkse zorg – hoe doe jij dit?",
     "Rust, nabijheid en veilige verzorging."),
    ("Ontwikkelingsstimulering – hoe doe jij dit?",
     "Observeren en aansluiten bij ontwikkeling."),
    ("Oudercommunicatie – hoe doe jij dit?",
     "Warm, eerlijk en open communiceren."),
    ("Een ouder heeft een klacht. Hoe ga je ermee om?",
     "Luisteren, erkennen, melden."),
    ("Wat is klachtenprocedure?",
     "1) Ontvangst 2) Onderzoek 3) Terugkoppeling"),
    ("Wat is grensoverschrijdend gedrag?",
     "Fysiek of verbaal geweld, negeren, vernederen."),
    ("Crisisprocedures – stappen?",
     "1) Alarmeren 2) Hulpdiensten 3) Veiligheid"),
    ("Hoe zijn leefgroepen ingedeeld?",
     "Baby's → verzorging; peuters → taal & structuur."),
    ("Hoe doe je toezicht op rustruimtes?",
     "Elke 10–15 min fysieke controle."),
    ("Welke risico’s zijn er in opvang?",
     "Risico-analyse in rode map.")
]


# =============================================================
# SESSION STATE
# =============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "score" not in st.session_state:
    st.session_state.score = 0

if "max_score" not in st.session_state:
    st.session_state.max_score = len(pikler_mc) + len(pikler_open) + len(vragen_A) + len(vragen_B)

if "idx" not in st.session_state:
    st.session_state.idx = 0

if "substep" not in st.session_state:
    st.session_state.substep = 1  # 1 = MC, 2 = open vraag bij Pikler


# =============================================================
# GENERIC QUESTION RENDERERS
# =============================================================

def run_mc_module(questions, module_name, next_step_function):
    show_feedback()

    i = st.session_state.idx
    if i >= len(questions):
        st.session_state.idx = 0
        st.session_state.last_fb = None   # feedback eerst leegmaken
        next_step_function()              # ga door naar open vraag
        st.rerun()                        # LAATSTE stap: herlaad app
        return

    vraag, opties, juist, uitleg = questions[i]
    st.title(module_name)
    st.write(vraag)

    keuze = st.radio("Kies:", opties, key=f"radio_{module_name}_{i}")

    if st.button("Controleer", key=f"btn_mc_{module_name}_{i}"):
        if keuze == juist:
            st.session_state.score += 1
            store_feedback("success", "Juist!", uitleg)
        else:
            store_feedback("error", f"Fout. Juiste antwoord is: {juist}", uitleg)

        st.session_state.idx += 1
        st.rerun()


def run_open_module(questions, module_name, back_to_home=False, next_step_function=None):
    show_feedback()

    i = st.session_state.idx
    if i >= len(questions):
        st.session_state.idx = 0
        if back_to_home:
            st.session_state.page = "home"
        elif next_step_function:
            next_step_function()
        st.rerun()
        return

    vraag, model = questions[i]
    st.title(module_name)
    st.write(vraag)

    ans = st.text_area("Jouw antwoord:", key=f"txt_{module_name}_{i}")

    if st.button("Controleer", key=f"btn_open_{module_name}_{i}"):
        if ans.strip() != "":
            st.session_state.score += 1

        store_feedback("success", "Modelantwoord:", model)
        st.session_state.idx += 1
        st.rerun()


# =============================================================
# PAGE ROUTING
# =============================================================

# HOME
if st.session_state.page == "home":
    st.title("🌱 Zorgpunt Meetjesland – Vragenlijsten")

    if st.button("➡️ Module 1: Emmi Pikler"):
        st.session_state.page = "m1_mc"
        st.session_state.idx = 0

    if st.button("➡️ Module 2: Vragenlijst A"):
        st.session_state.page = "m2"
        st.session_state.idx = 0

    if st.button("➡️ Module 3: Vragenlijst B"):
        st.session_state.page = "m3"
        st.session_state.idx = 0

    # Certificaat beschikbaar zodra er punten zijn
    if st.session_state.score > 0:
        st.subheader("📜 Certificaat genereren")
        name = st.text_input("Naam:")

        if name:
            html = cert_html(name, st.session_state.score, st.session_state.max_score)
            st.download_button("📄 Download certificaat", html, "certificaat.html", "text/html")


# MODULE 1 — Pikler (MC)
elif st.session_state.page == "m1_mc":
    run_mc_module(pikler_mc, "Module 1 – Emmi Pikler", next_step_function=lambda: setattr(st.session_state, "page", "m1_open"))

# MODULE 1 — Pikler (OPEN)
elif st.session_state.page == "m1_open":
    run_open_module(pikler_open, "Module 1 – Emmi Pikler (Open Vraag)", next_step_function=lambda: setattr(st.session_state, "page", "home"))

# MODULE 2 — A
elif st.session_state.page == "m2":
    run_open_module(vragen_A, "Module 2 – Vragenlijst A", next_step_function=lambda: setattr(st.session_state, "page", "home"))

# MODULE 3 — B
elif st.session_state.page == "m3":
    run_open_module(vragen_B, "Module 3 – Vragenlijst B", next_step_function=lambda: setattr(st.session_state, "page", "home"))

