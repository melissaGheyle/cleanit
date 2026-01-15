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
        <h2>{name}</h2>
        <p>Score: {score}/{max_score} ({perc}%)</p>
        <h3>{status}</h3>
        <p>Datum: {today}</p>
        <p>Code: <b>{generate_code()}</b></p>
    </body>
    </html>
    """

def feedback():
    fb = st.session_state.get("feedback")
    if fb:
        st.success(fb)
        st.session_state.feedback = None


# =============================================================
# VRAGEN
# =============================================================

pikler_mc = [
    ("Wat is het belangrijkste principe van de Emmi Pikler-visie?",
     ["A. Snel leren", "B. Begeleider stuurt", "C. Kind op eigen tempo", "D. Ouders bepalen"],
     "C. Kind op eigen tempo"),
    ("Hoe draagt Zorgpunt bij aan een rustige sfeer?",
     ["A. Kinderliedjes", "B. Hout & tapijten", "C. Alles wegbergen", "D. Felle kleuren"],
     "B. Hout & tapijten"),
]

pikler_open = [
    ("Hoe stimuleert Zorgpunt zelfstandigheid?",
     "Door materiaal op kindhoogte, keuzes bieden en kinderen actief te betrekken.")
]

vragen_A = [
    ("Wat is welbevinden en betrokkenheid?",
     "Welbevinden = hoe goed een kind zich voelt; betrokkenheid = hoe diep het speelt.")
]

vragen_B = [
    ("Wat is grensoverschrijdend gedrag?",
     "Fysiek of verbaal geweld, negeren, vernederen.")
]

# =============================================================
# SESSION STATE
# =============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "done_m1" not in st.session_state:
    st.session_state.done_m1 = False
if "done_m2" not in st.session_state:
    st.session_state.done_m2 = False
if "done_m3" not in st.session_state:
    st.session_state.done_m3 = False

st.session_state.max_score = len(pikler_mc) + len(pikler_open) + len(vragen_A) + len(vragen_B)

# =============================================================
# MODULE FUNCTIES
# =============================================================

def run_mc(questions, next_page):
    feedback()
    i = st.session_state.idx

    if i >= len(questions):
        st.session_state.idx = 0
        st.session_state.page = next_page
        st.rerun()

    vraag, opties, juist = questions[i]
    st.write(vraag)

    keuze = st.radio("Kies:", opties, key=f"mc_{i}")

    if st.button("Controleer", key=f"mc_btn_{i}"):
        if keuze == juist:
            st.session_state.score += 1
            st.session_state.feedback = "Juist!"
        else:
            st.session_state.feedback = f"Fout. Correct antwoord: {juist}"

        st.session_state.idx += 1
        st.rerun()


def run_open(questions, done_flag):
    feedback()
    i = st.session_state.idx

    if i >= len(questions):
        st.session_state.idx = 0
        st.session_state[done_flag] = True
        st.session_state.page = "home"
        st.rerun()

    vraag, model = questions[i]
    st.write(vraag)
    ans = st.text_area("Antwoord:", key=f"open_{i}")

    if st.button("Controleer", key=f"open_btn_{i}"):
        if ans.strip():
            st.session_state.score += 1
        st.session_state.feedback = f"Modelantwoord: {model}"
        st.session_state.idx += 1
        st.rerun()

# =============================================================
# PAGINA'S
# =============================================================

if st.session_state.page == "home":
    st.title("🌱 Zorgpunt Meetjesland – Vragenlijsten")

    if st.button("Module 1 – Emmi Pikler"):
        st.session_state.page = "m1_mc"
        st.session_state.idx = 0
        st.rerun()

    if st.button("Module 2 – Vragenlijst A"):
        st.session_state.page = "m2"
        st.session_state.idx = 0
        st.rerun()

    if st.button("Module 3 – Vragenlijst B"):
        st.session_state.page = "m3"
        st.session_state.idx = 0
        st.rerun()

    if st.session_state.done_m1 and st.session_state.done_m2 and st.session_state.done_m3:
        name = st.text_input("Naam voor certificaat")
        if name:
            html = cert_html(name, st.session_state.score, st.session_state.max_score)
            st.download_button("Download certificaat", html, "certificaat.html", "text/html")

elif st.session_state.page == "m1_mc":
    st.title("Module 1 – Emmi Pikler (MC)")
    run_mc(pikler_mc, "m1_open")

elif st.session_state.page == "m1_open":
    st.title("Module 1 – Emmi Pikler (Open)")
    run_open(pikler_open, "done_m1")

elif st.session_state.page == "m2":
    st.title("Module 2 – Vragenlijst A")
    run_open(vragen_A, "done_m2")

elif st.session_state.page == "m3":
    st.title("Module 3 – Vragenlijst B")
    run_open(vragen_B, "done_m3")
