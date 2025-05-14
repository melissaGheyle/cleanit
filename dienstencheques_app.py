import streamlit as st
from datetime import datetime
import math

st.set_page_config(page_title="Dienstencheque App", layout="centered")
st.title("🧾 Dienstencheque Calculator")

# Inputvelden
starttijd = st.text_input("Starttijd (vb: 08:00)", "08:00")
eindtijd = st.text_input("Eindtijd (vb: 11:00)", "11:00")
tegoed_vorig = st.number_input("Tegoed vorige keer (in minuten)", min_value=0, value=0, step=1)

if st.button("Bereken"):
    try:
        start = datetime.strptime(starttijd, "%H:%M")
        einde = datetime.strptime(eindtijd, "%H:%M")
        verschil = (einde - start).seconds / 60 + 20  # +20 minuten standaard

        netto_minuten = verschil - tegoed_vorig

        if netto_minuten <= 0:
            cheques = 0
            nieuw_tegoed = netto_minuten  # negatief tegoed
        else:
            cheques = math.ceil(netto_minuten / 60)
            nieuw_tegoed = (cheques * 60) - netto_minuten

        st.subheader("📋 Resultaat")
        st.write(f"**Totaal minuten (incl. 20 extra):** {int(verschil)}")
        st.write(f"**Tegoed vorige keer:** {int(tegoed_vorig)} min")
        st.write(f"**Netto minuten:** {int(max(0, netto_minuten))}")
        st.write(f"**Dienstencheques:** {cheques}")
        st.write(f"**Nieuw berekend tegoed:** {int(nieuw_tegoed)} minuten")

        if nieuw_tegoed < 0:
            st.markdown(f"<span style='color:red;'>**Saldo verschil: {int(nieuw_tegoed)} minuten**</span>", unsafe_allow_html=True)
        elif nieuw_tegoed > 0:
            st.markdown(f"<span style='color:blue;'>**Tegoed verschil: +{int(nieuw_tegoed)} minuten**</span>", unsafe_allow_html=True)

    except Exception as e:
        st.error("❌ Fout: Controleer of de tijden correct zijn ingevoerd als HH:MM.")
