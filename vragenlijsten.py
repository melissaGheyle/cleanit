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

    antwoorden_html = ""

    for a in st.session_state.answers:
        antwoorden_html += f"""
        <p>
        <b>Vraag:</b> {a['vraag']}<br>
        <b>Jouw antwoord:</b> {a['gegeven']}<br>
        <b>Correct antwoord:</b> {a['correct']}
        </p>
        <hr>
        """

    return f"""
    <html>
    <body style="font-family:Arial; padding:40px;">

        <h1 style="text-align:center;">Certificaat van Deelname</h1>

        <h3>Uitgereikt aan:</h3>
        <h2>{name}</h2>

        <p>na het afronden van alle pedagogische modules<br>Zorgpunt Meetjesland</p>

        <h3>Score: {score} / {max_score} ({perc}%)</h3>
        <h2>{status}</h2>

        <p>Datum: {today}</p>
        <p>Unieke verificatiecode: <b>{generate_code()}</b></p>

        <br><hr><br>

        <h2>Overzicht antwoorden</h2>

        {antwoorden_html}

        <br><hr><br>
        <p><i>Zorgpunt Meetjesland – Bevestiging van deelname</i></p>

    </body>
    </html>
    """

def store_feedback(msg_type, msg_main, explanation):
    st.session_state.last_fb = (msg_type, msg_main, explanation)

def show_feedback():
    fb = st.session_state.get("last_fb", None)
    if not fb or not isinstance(fb, tuple) or len(fb) != 3:
        return

    fb_type, fb_msg, fb_expl = fb

    if fb_type == "success":
        st.success(fb_msg)
    else:
        st.error(fb_msg)

    st.info(fb_expl)
    st.session_state.last_fb = None

def point_if_filled(text):
    return 1 if text.strip() != "" else 0


# =============================================================
# VRAGEN
# =============================================================

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

pikler_open = [
("Hoe stimuleert Zorgpunt zelfstandigheid?",
"Door materiaal op kindhoogte te zetten, keuzes te bieden en kinderen actief te betrekken.")
]

vragen_A = [


# -------------------------------------------------
# WELBEVINDEN
# -------------------------------------------------

("Wat betekent welbevinden bij een kind?",
"Welbevinden betekent dat een kind zich veilig, ontspannen en goed voelt in de opvang. Dit kan je zien aan gezichtsuitdrukking, spontaniteit, energie en lichaamshouding."),

("Welke signalen tonen hoog welbevinden bij een kind?",
"Een ontspannen houding, lachen, spontaan spelen, open contact met anderen en een gevoel van veiligheid."),

("Wat kan een begeleider doen wanneer het welbevinden van een kind laag is?",
"Observeren wat het kind nodig heeft, extra aandacht geven, veiligheid creëren en eventueel overleggen met collega's of ouders."),


# -------------------------------------------------
# BETROKKENHEID
# -------------------------------------------------

("Wat betekent betrokkenheid bij een kind?",
"Betrokkenheid betekent dat een kind intens geconcentreerd bezig is met een activiteit of spel."),

("Welke signalen tonen hoge betrokkenheid bij een kind?",
"Energie, concentratie, doorzettingsvermogen, creativiteit en enthousiasme tijdens het spelen."),

("Wat kan je doen wanneer de betrokkenheid van een kind laag is?",
"Aansluiten bij de interesses van het kind, uitdagend materiaal aanbieden en het spelaanbod aanpassen."),


# -------------------------------------------------
# EMOTIONELE ONDERSTEUNING
# -------------------------------------------------

("Wat betekent emotionele ondersteuning in de kinderopvang?",
"Kinderen veiligheid en vertrouwen geven door warme interacties, nabijheid en aandacht."),

("Hoe kan een begeleider emotionele ondersteuning bieden aan kinderen?",
"Door oogcontact, luisteren, geruststellen, reageren op signalen van het kind en een warme relatie op te bouwen."),

("Waarom is een veilige relatie tussen kind en begeleider belangrijk?",
"Een veilige relatie helpt kinderen zich veilig te voelen en ondersteunt hun emotionele en sociale ontwikkeling."),


# -------------------------------------------------
# EDUCATIEVE ONDERSTEUNING
# -------------------------------------------------

("Wat betekent educatieve ondersteuning in de kinderopvang?",
"Kinderen ondersteunen in hun ontwikkeling door spel, activiteiten en interactie."),

("Hoe kan een begeleider de ontwikkeling van kinderen stimuleren?",
"Door uitdagend spelmateriaal, activiteiten, vrij spel en interactie met kinderen."),

("Waarom is taalstimulering belangrijk bij baby's en peuters?",
"Taalstimulering helpt kinderen om te communiceren, relaties op te bouwen en zich cognitief te ontwikkelen."),


# -------------------------------------------------
# OMGEVING
# -------------------------------------------------

("Waarom is een veilige omgeving belangrijk in de kinderopvang?",
"Een veilige omgeving zorgt ervoor dat kinderen zonder risico's kunnen spelen en ontdekken."),

("Wat zijn kenmerken van een stimulerende speelomgeving?",
"Voldoende spelmateriaal, duidelijke speelhoeken, veiligheid en materialen aangepast aan de leeftijd."),

("Hoe kan de inrichting van een ruimte het spel van kinderen stimuleren?",
"Door verschillende speelhoeken, toegankelijk materiaal en een overzichtelijke en rustige inrichting."),


# -------------------------------------------------
# GEZINNEN EN DIVERSITEIT
# -------------------------------------------------

("Waarom is samenwerking met ouders belangrijk in de kinderopvang?",
"Ouders kennen hun kind het best en samenwerking helpt om beter in te spelen op de behoeften van het kind."),

("Hoe kan een begeleider een goede relatie met ouders opbouwen?",
"Door open communicatie, respect, dagelijkse overdrachten en luisteren naar ouders."),

("Wat betekent respect voor diversiteit in de kinderopvang?",
"Rekening houden met verschillende culturen, talen, achtergronden en waarden van gezinnen.")

]

vragen_B = [
("Dagelijkse zorg – hoe doe jij dit?",
"Rust en veilige verzorging."),
("Ontwikkelingsstimulering – hoe doe jij dit?",
"Door passend materiaal en spel."),
("Oudercommunicatie – hoe doe jij dit?",
"Warm en open communiceren."),
("Een ouder heeft een klacht. Hoe ga je ermee om?",
"Luisteren en melden."),
("Wat is klachtenprocedure?",
"Ontvangst – onderzoek – terugkoppeling."),
("Wat is grensoverschrijdend gedrag?",
"Fysiek of verbaal geweld."),
("Crisisprocedures – stappen?",
"Alarmeren – hulpdiensten – communicatie."),
("Hoe zijn leefgroepen ingedeeld?",
"Baby's verzorging, peuters structuur."),
("Hoe doe je toezicht op rustruimtes?",
"Elke 10–15 minuten controleren."),
("Welke risico’s zijn er in opvang?",
"Risicoanalyse.")
]

# =============================================================
# SESSION STATE
# =============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "score" not in st.session_state:
    st.session_state.score = 0

if "idx" not in st.session_state:
    st.session_state.idx = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "done_m1" not in st.session_state:
    st.session_state.done_m1 = False

if "done_m2" not in st.session_state:
    st.session_state.done_m2 = False

if "done_m3" not in st.session_state:
    st.session_state.done_m3 = False

st.session_state.max_score = len(pikler_mc) + len(pikler_open) + len(vragen_A) + len(vragen_B)

# =============================================================
# MODULE RUNNERS
# =============================================================

def run_mc_module(questions, module_name, next_step_function):
    show_feedback()

    i = st.session_state.idx

    if i >= len(questions):
        st.session_state.idx = 0
        st.session_state.last_fb = None
        next_step_function()
        st.rerun()

    vraag, opties, juist, uitleg = questions[i]

    st.title(module_name)
    st.write(vraag)

    keuze = st.radio("Kies:", opties, key=f"radio_{module_name}_{i}")

    if st.button("Controleer", key=f"btn_mc_{module_name}_{i}"):

        st.session_state.answers.append({
            "vraag": vraag,
            "gegeven": keuze,
            "correct": juist
        })

        if keuze == juist:
            st.session_state.score += 1
            store_feedback("success", "Juist!", uitleg)
        else:
            store_feedback("error", f"Fout. Juiste antwoord is: {juist}", uitleg)

        st.session_state.idx += 1
        st.rerun()


def run_open_module(questions, module_name, finish_flag):
    show_feedback()

    i = st.session_state.idx

    if i >= len(questions):
        st.session_state.idx = 0
        st.session_state[finish_flag] = True
        st.session_state.last_fb = None
        st.session_state.page = "home"
        st.rerun()

    vraag, model = questions[i]

    st.title(module_name)
    st.write(vraag)

    ans = st.text_area("Jouw antwoord:", key=f"txt_{module_name}_{i}")

    if st.button("Controleer", key=f"btn_open_{module_name}_{i}"):

        st.session_state.answers.append({
            "vraag": vraag,
            "gegeven": ans,
            "correct": model
        })

        if ans.strip() != "":
            st.session_state.score += 1

        store_feedback("success", "Modelantwoord:", model)

        st.session_state.idx += 1
        st.rerun()

# =============================================================
# PAGE ROUTING
# =============================================================

if st.session_state.page == "home":

    st.title("🌱 Zorgpunt Meetjesland – Vragenlijsten")

    if not st.session_state.done_m1:
        st.info("🔒 Rond eerst Module 1 af om Module 2 en 3 te openen.")

    if st.button("➡️ Module 1: Emmi Pikler"):
        st.session_state.page = "m1_mc"
        st.session_state.idx = 0

    if st.button("➡️ Module 2: Vragenlijst MEMOQ", disabled=not st.session_state.done_m1):
        st.session_state.page = "m2"
        st.session_state.idx = 0

    if st.button("➡️ Module 3: Vragenlijst MIJN OPVANG", disabled=not st.session_state.done_m1):
        st.session_state.page = "m3"
        st.session_state.idx = 0

    if st.session_state.done_m1 and st.session_state.done_m2 and st.session_state.done_m3:

        st.subheader("📜 Certificaat genereren")

        name = st.text_input("Naam:")

        if name:
            html = cert_html(name, st.session_state.score, st.session_state.max_score)

            st.download_button(
                "📄 Download certificaat",
                html,
                "certificaat.html",
                "text/html"
            )


elif st.session_state.page == "m1_mc":

    run_mc_module(
        pikler_mc,
        "Module 1 – Emmi Pikler",
        next_step_function=lambda: setattr(st.session_state, "page", "m1_open")
    )


elif st.session_state.page == "m1_open":

    run_open_module(
        pikler_open,
        "Module 1 – Emmi Pikler (Open Vraag)",
        finish_flag="done_m1"
    )


elif st.session_state.page == "m2":

    run_open_module(
        vragen_A,
        "Module 2 – Vragenlijst A",
        "done_m2"
    )


elif st.session_state.page == "m3":

    run_open_module(
        vragen_B,
        "Module 3 – Vragenlijst B",
        "done_m3"
    )


