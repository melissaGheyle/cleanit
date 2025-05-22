import streamlit as st

st.set_page_config(page_title="Controle per regio", layout="wide")
st.title("📊 Arbeidsmarktindicatoren per regio")

st.markdown("Vul de vijf gegevens per regio in. Klik op **Controleer invoer** om je antwoorden te vergelijken met de officiële cijfers van 2024.")

# ✅ Officiële cijfers per regio
officieel = {
    "Wallonië": {
        "Werklozen": 129003,
        "Werkenden": 1297081,
        "Niet-actieven": 1048984,
    },
    "Vlaanderen": {
        "Werklozen": 121617,
        "Werkenden": 3090288,
        "Niet-actieven": 1806096,
    },
    "Brussel": {
        "Werklozen": 68380,
        "Werkenden": 512631,
        "Niet-actieven": 361920,
    }
}

# 🔁 Bereken afgeleide cijfers + indicatoren
def bereken_indicatoren(data):
    wl = data["Werklozen"]
    wn = data["Werkenden"]
    na = data["Niet-actieven"]
    bb = wl + wn
    al = bb + na
    data["Beroepsbevolking"] = bb
    data["Bevolking op arbeidsleeftijd"] = al
    data["Werkloosheidsgraad"] = round((wl / bb) * 100, 1) if bb else 0.0
    data["Activiteitsgraad"] = round((bb / al) * 100, 1) if al else 0.0
    data["Werkzaamheidsgraad"] = round((wn / al) * 100, 1) if al else 0.0

for regio in officieel:
    bereken_indicatoren(officieel[regio])

# 📥 Invoer door gebruiker
def invoervelden(regio, prefix, default, emoji):
    st.subheader(f"{emoji} {regio}")
    wl = st.number_input("Werklozen", key=f"{prefix}_wl", value=default[0], step=1000)
    wn = st.number_input("Werkenden", key=f"{prefix}_wn", value=default[1], step=1000)
    na = st.number_input("Niet-actieven", key=f"{prefix}_na", value=default[2], step=1000)
    bb = wl + wn
    al = bb + na

    if wl > 0 and wn > 0 and na > 0:
        wlgr = round((wl / bb) * 100, 1) if bb else 0.0
        actgr = round((bb / al) * 100, 1) if al else 0.0
        wzgr = round((wn / al) * 100, 1) if al else 0.0
    else:
        wlgr = actgr = wzgr = None  # Graden niet ton
