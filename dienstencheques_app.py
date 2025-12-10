import streamlit as st
from datetime import datetime
import math

st.set_page_config(page_title="Dienstencheque calculator", layout="centered")
st.title("🧾 Dienstencheque calculator")

# Inputvelden
starttijd = st.text_input("Starttijd (vb: 08:00)", "08:00")
eindtijd = st.text_input("Eindtijd (vb: 11:30)", "11:30")
tegoed_input = st.text_input("Tegoed vorige keer (in minuten)", "0")

if st.button("Bereken"):
    foutmelding = None

    # Tijd-validatie
    try:
        start = datetime.strptime(starttijd.strip(), "%H:%M")
        einde = datetime.strptime(eindtijd.strip(), "%H:%M")
    except ValueError:
        foutmelding = "❌ Start- en eindtijd moeten in HH:MM-formaat zijn (bv. 08:00)."

    # Tijdvolgorde controleren
    if foutmelding is None and einde <= start:
        foutmelding = "❌ De eindtijd moet later zijn dan de starttijd."

    # Tegoed-validatie
    if foutmelding is None and not tegoed_input.strip().isdigit():
        foutmelding = "❌ Tegoed moet een positief geheel getal zijn (bv. 30)."

    if foutmelding:
        st.error(foutmelding)
    else:
        tegoed = int(tegoed_input)

        # Ruwe werkduur
        gewerkte_minuten = int((einde - start).seconds / 60)

        # Nieuwe regel: per 60 min → +10 min
        extra_minuten = (gewerkte_minuten // 60) * 10

        # Totale minuten incl. extra
        totaal_minuten = gewerkte_minuten + extra_minuten

        # Netto berekening
        netto_minuten = totaal_minuten - tegoed

        if netto_minuten <= 0:
            cheques = 0
            nieuw_tegoed = netto_minuten
        else:
            cheques = math.ceil(netto_minuten / 60)
            nieuw_tegoed = (cheques * 60) - netto_minuten

        st.subheader("📋 Resultaat")
        st.text(f"""
Gewerkte minuten: {gewerkte_minuten}
Extra minuten (+10 per 60 min): {extra_minuten}
Totaal minuten: {totaal_minuten}

- Tegoed vorige keer: {tegoed} min
= Netto minuten: {int(max(0, netto_minuten))}

Dienstencheques: {cheques}
Nieuw berekend tegoed: {int(nieuw_tegoed)} minuten
""")

        # Tegoedverschil tonen
        if nieuw_tegoed < 0:
            st.markdown(f"<span style='color:red;'>**Saldo verschil: {int(nieuw_tegoed)} minuten**</span>", unsafe_allow_html=True)
        elif nieuw_tegoed > 0:
            st.markdown(f"<span style='color:blue;'>**Tegoed verschil: +{int(nieuw_tegoed)} minuten**</span>", unsafe_allow_html=True)
