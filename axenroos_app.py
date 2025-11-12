# axenroos_app.py (versie 6 - stabiele sliders + sessiebehoud)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="Axenroos Communicatietool", layout="wide")

st.title("🌸 Axenroos Communicatietool (stabiele versie)")
st.write("""
Beantwoord de stellingen eerlijk op een schaal van **1 (helemaal niet van toepassing)** tot **5 (helemaal van toepassing)**.  
De vragen verschijnen in willekeurige volgorde, maar blijven stabiel zodat je antwoorden bewaard blijven.
""")

# --- 1. Verkorte vragen per ax (3 per profiel) -------------------------------
vragen_dict = {
    "Leeuw": [
        "Ik neem spontaan het voortouw in een groep.",
        "Ik geef duidelijk richting aan anderen.",
        "Ik spreek iemand aan als iets niet goed loopt."
    ],
    "Kameel": [
        "Ik voel me comfortabel als iemand anders beslist.",
        "Ik volg graag afspraken en regels.",
        "Ik ben loyaal tegenover leidinggevenden."
    ],
    "Bever": [
        "Ik bied hulp aan zonder dat iemand het vraagt.",
        "Ik voel me verantwoordelijk voor de sfeer.",
        "Ik merk het snel als iemand zich niet goed voelt."
    ],
    "Kat": [
        "Ik durf hulp te vragen.",
        "Ik kan genieten van zorg of aandacht van anderen.",
        "Ik geef aan wanneer ik behoefte heb aan steun."
    ],
    "Pauw": [
        "Ik vertel graag over dingen die ik goed doe.",
        "Ik ben trots op mijn werk.",
        "Ik geniet ervan als mensen mijn talenten zien."
    ],
    "Hond": [
        "Ik geef graag complimenten.",
        "Ik toon waardering voor anderen.",
        "Ik zeg het als ik trots ben op iemand."
    ],
    "Havik": [
        "Ik zeg het als ik het ergens niet mee eens ben.",
        "Ik verdedig mijn standpunt met overtuiging.",
        "Ik durf grenzen te stellen."
    ],
    "Schildpad": [
        "Ik vermijd liever ruzie dan die aan te gaan.",
        "Ik trek me terug als het te gespannen wordt.",
        "Ik voel me ongemakkelijk bij confrontaties."
    ],
    "Uil": [
        "Ik geloof dat mensen goede bedoelingen hebben.",
        "Ik durf fouten toe te geven.",
        "Ik vertrouw erop dat afspraken worden nagekomen."
    ],
    "Wasbeer": [
        "Ik hou afstand tot mensen tot ik ze beter ken.",
        "Ik ben voorzichtig met persoonlijke informatie.",
        "Ik observeer liever dan meteen te praten."
    ],
    "Steenbok": [
        "Ik heb tijd voor mezelf nodig om op te laden.",
        "Ik neem beslissingen liever zelfstandig.",
        "Ik hou ervan om mijn grenzen te bewaken."
    ],
    "Duif": [
        "Ik zoek makkelijk contact met anderen.",
        "Ik voel me goed in gezelschap.",
        "Ik geniet van samenwerken."
    ]
}

# --- 2. Genereer en bewaar willekeurige volgorde ----------------------------
if "vragen_volgorde" not in st.session_state:
    alle_vragen = []
    for ax, lijst in vragen_dict.items():
        for vraag in lijst:
            alle_vragen.append({"ax": ax, "vraag": vraag})
    random.shuffle(alle_vragen)
    st.session_state["vragen_volgorde"] = alle_vragen
else:
    alle_vragen = st.session_state["vragen_volgorde"]

# --- 3. Antwoorden verzamelen -----------------------------------------------
if "antwoorden" not in st.session_state:
    st.session_state["antwoorden"] = {}

scores = {ax: 0 for ax in vragen_dict.keys()}
antwoord_teller = 0

st.subheader("🧾 Vragenlijst")
for i, item in enumerate(alle_vragen, 1):
    key = f"vraag_{i}"
    if key not in st.session_state["antwoorden"]:
        st.session_state["antwoorden"][key] = None

    val = st.select_slider(
        f"{i}. {item['vraag']}",
        options=[None, 1, 2, 3, 4, 5],
        value=st.session_state["antwoorden"][key],
        format_func=lambda x: "Kies..." if x is None else str(x),
        key=key
    )

    # Sla keuze op
    st.session_state["antwoorden"][key] = val
    if val is not None:
        antwoord_teller += 1
        scores[item["ax"]] += val

# --- 4. Resultaten pas tonen na invulling -----------------------------------
totaal_vragen = len(alle_vragen)
progress = antwoord_teller / totaal_vragen
st.progress(progress)
st.write(f"Je hebt {antwoord_teller} van {totaal_vragen} vragen ingevuld ({progress:.0%}).")

if antwoord_teller < totaal_vragen:
    st.info("🕐 Beantwoord eerst alle vragen. De resultaten verschijnen automatisch zodra je klaar bent.")
    st.stop()

# --- 5. Berekeningen --------------------------------------------------------
df = pd.DataFrame(scores, index=["Totaal"]).T
df["Gemiddelde"] = df["Totaal"] / 3
df = df.sort_values(by="Gemiddelde", ascending=False)

st.header("📊 Resultaten")
st.dataframe(df[["Gemiddelde"]])

# Radar chart
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
categories = list(df.index)
values = df["Gemiddelde"].tolist()
N = len(categories)
values += values[:1]
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

ax.plot(angles, values, linewidth=2)
ax.fill(angles, values, alpha=0.25)
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=9)
ax.set_title("Jouw Axenroos-profiel", size=14, weight='bold', pad=20)
st.pyplot(fig)

# --- 6. Automatische interpretatie ------------------------------------------
top2 = df["Gemiddelde"].head(2)
ax1, ax2 = top2.index[0], top2.index[1]

profiel_duos = {
    ("Bever", "Duif"): ("💗 Warm verbinder", 
        "**🪞 Kern:** Je bent warm, empathisch en verbindend. Je brengt harmonie, biedt zorg en maakt mensen op hun gemak.  \n"
        "**⚖️ Spanning:** Je kunt te veel energie steken in anderen en jezelf vergeten. Soms vermijd je moeilijke gesprekken om de sfeer goed te houden.  \n"
        "**🌱 Groei:** Leer gezonde grenzen stellen en nee zeggen — zorg delen maakt je nog sterker."),
    ("Bever", "Hond"): ("🫶 Zorgzame ondersteuner",
        "**🪞 Kern:** Je toont waardering, biedt hulp en werkt graag samen. Mensen voelen zich veilig bij jou.  \n"
        "**⚖️ Spanning:** Je kunt te afhankelijk worden van bevestiging of de waardering van anderen.  \n"
        "**🌱 Groei:** Blijf jezelf waarderen — zelfzorg is even belangrijk als zorg voor anderen."),
    ("Leeuw", "Havik"): ("🦁 Beslist leider",
        "**🪞 Kern:** Je bent direct, assertief en daadkrachtig. Je zegt wat anderen denken en brengt duidelijkheid.  \n"
        "**⚖️ Spanning:** Soms kun je te snel of te scherp optreden, wat spanning veroorzaakt.  \n"
        "**🌱 Groei:** Ontwikkel je luistervaardigheid en toon empathie — zo blijft je kracht constructief."),
    ("Leeuw", "Bever"): ("🧭 Mensgerichte leider",
        "**🪞 Kern:** Je combineert richting en warmte. Je bent een natuurlijke leider die anderen motiveert met vertrouwen.  \n"
        "**⚖️ Spanning:** De zorgzame kant kan soms botsen met de behoefte aan controle.  \n"
        "**🌱 Groei:** Leer delegeren met vertrouwen — laat ruimte voor anderen om te groeien."),
    ("Leeuw", "Uil"): ("🦉 Strategische leider",
        "**🪞 Kern:** Je denkt en handelt met visie. Je hebt de kracht om richting te geven én de rust om na te denken.  \n"
        "**⚖️ Spanning:** Je neigt soms naar perfectionisme of analyseverlamming.  \n"
        "**🌱 Groei:** Vertrouw op je intuïtie — niet alles hoeft rationeel te zijn om juist te voelen."),
    ("Kameel", "Steenbok"): ("🐫 Betrouwbare uitvoerder",
        "**🪞 Kern:** Je bent loyaal, zelfstandig en standvastig. Mensen weten wat ze aan je hebben.  \n"
        "**⚖️ Spanning:** Je neemt zelden het initiatief of risico’s, waardoor kansen kunnen voorbijgaan.  \n"
        "**🌱 Groei:** Durf uit je comfortzone te komen — initiatief tonen versterkt je betrouwbaarheid."),
    ("Pauw", "Duif"): ("🦚 Charismatische verbinder",
        "**🪞 Kern:** Je bent enthousiast, sociaal en brengt positieve energie. Je laat mensen zich gezien voelen.  \n"
        "**⚖️ Spanning:** Je zoekt soms te veel bevestiging of wil te graag dat iedereen je leuk vindt.  \n"
        "**🌱 Groei:** Richt je op authentieke verbinding — niet iedereen hoeft overtuigd te worden om je te waarderen."),
    ("Hond", "Duif"): ("🐶 Positieve samenwerker",
        "**🪞 Kern:** Je creëert harmonie, waardeert anderen en werkt verbindend. Je bent de lijm in teams.  \n"
        "**⚖️ Spanning:** Je kunt conflicten vermijden en spanning onder de mat schuiven.  \n"
        "**🌱 Groei:** Leer je grenzen aangeven en opkomen voor je eigen noden."),
    ("Wasbeer", "Steenbok"): ("🦝 Onafhankelijke denker",
        "**🪞 Kern:** Je bent rustig, analytisch en bedachtzaam. Je hebt oog voor detail en consistentie.  \n"
        "**⚖️ Spanning:** Je kunt afstandelijk of moeilijk benaderbaar lijken.  \n"
        "**🌱 Groei:** Deel je inzichten vaker met anderen — ze waarderen je observatievermogen."),
    ("Havik", "Uil"): ("⚖️ Eerlijke verdediger",
        "**🪞 Kern:** Je bent principieel, assertief en oprecht. Je verdedigt wat juist is, ook voor anderen.  \n"
        "**⚖️ Spanning:** Soms kun je te kritisch zijn of te veel rechtlijnigheid tonen.  \n"
        "**🌱 Groei:** Voeg zachtheid toe aan je kracht — eerlijkheid wint meer met empathie."),
    ("Schildpad", "Kameel"): ("🐢 Vreedzame helper",
        "**🪞 Kern:** Je bent rustig, loyaal en conflictmijdend. Je zoekt harmonie en stabiliteit.  \n"
        "**⚖️ Spanning:** Je zegt niet altijd wat je denkt, waardoor misverstanden kunnen ontstaan.  \n"
        "**🌱 Groei:** Assertiever communiceren helpt je harmonie juist te behouden."),
}

def find_duo(ax1, ax2):
    for combo, (titel, tekst) in profiel_duos.items():
        if set(combo) == set((ax1, ax2)):
            return titel, tekst
    return (f"✨ Gemengd profiel: {ax1} & {ax2}",
            f"Je combineert de eigenschappen van **{ax1}** en **{ax2}**. "
            f"Dat betekent dat je flexibel communiceert en je stijl aanpast aan de situatie.")

titel, uitleg = find_duo(ax1, ax2)

st.header("🧠 Jouw communicatiestijl")
st.subheader(titel)
st.markdown(uitleg)

st.markdown("### 🌱 Wat kun je hieruit leren?")
st.write("""
- Je twee dominante stijlen zijn jouw natuurlijke krachtbronnen.  
- Te veel nadruk op één kant kan spanning veroorzaken (bv. te veel geven, te weinig grenzen).  
- Communicatieve groei = leren **schakelen** tussen stijlen afhankelijk van de context.  
- Observeer hoe je reageert bij stress of in groepen — dan komt je 'basisdier' het sterkst naar voren.  
""")
