import streamlit as st
from datetime import datetime
import math

st.set_page_config(page_title="Dienstencheque Calculator", layout="centered")
st.title("🧾 Dienstencheque Calculator")

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
        verschil = (einde - start).seconds / 60 + 20  # extra 20 min

        netto_minuten = verschil - tegoed

        if netto_minuten <= 0:
            cheques = 0
            nieuw_tegoed = netto_minuten
        else:
            cheques = math.ceil(netto_minuten / 60)
            nieuw_tegoed = (cheques * 60) - netto_minuten

        st.subheader("📋 Resultaat")
        st.text(f"""
Totaal minuten (incl. +20 min): {int(verschil)}
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
