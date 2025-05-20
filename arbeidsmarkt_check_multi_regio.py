import streamlit as st

# Officiële waarden België 2023 volgens Excelbestand
officiele = {
    "Werklozen": 306179,
    "Werkenden": 5056315,
    "Niet-actieven": 3335799,
    "Beroepsbevolking": 5362494,  # werkenden + werklozen
    "Bevolking op arbeidsleeftijd": 8698293  # beroepsbevolking + niet-actieven
}

st.set_page_config(page_title="Controle per regio", layout="wide")
st.title("📊 Arbeidsmarktindicatoren per regio")
st.markdown("Vul de 5 basisgegevens in per regio. De indicatoren worden automatisch berekend en gecontroleerd.")

def toon_indicatoren(regio, werklozen, werkenden, niet_actieven, beroepsbevolking, arbeidsleeftijd, referentie=None):
    st.markdown(f"### 📍 {regio}")

    def check(ingave, ref):
        return "✔️" if ingave == ref else f"❌ ({ref})"

    try:
        wlgr = round((werklozen / beroepsbevolking) * 100, 1)
    except ZeroDivisionError:
        wlgr = 0.0

    try:
        actgr = round((beroepsbevolking / arbeidsleeftijd) * 100, 1)
    except ZeroDivisionError:
        actgr = 0.0

    try:
        wzgr = round((werkenden / arbeidsleeftijd) * 100, 1)
    except ZeroDivisionError:
        wzgr = 0.0

    st.markdown("#### 🧮 Berekende indicatoren")
    st.metric(label="📉 Werkloosheidsgraad", value=f"{wlgr} %")
    st.metric(label="📊 Activiteitsgraad", value=f"{actgr} %")
    st.metric(label="💼 Werkzaamheidsgraad", value=f"{wzgr} %")

    if referentie:
        st.markdown("#### 🔍 Controle ingevoerde cijfers (tegen officiële cijfers België 2023)")
        st.write(f"- Werklozen: {werklozen} {check(werklozen, referentie['Werklozen'])}")
        st.write(f"- Werkenden: {werkenden} {check(werkenden, referentie['Werkenden'])}")
        st.write(f"- Niet-actieven: {niet_actieven} {check(niet_actieven, referentie['Niet-actieven'])}")
        st.write(f"- Beroepsbevolking: {beroepsbevolking} {check(beroepsbevolking, referentie['Beroepsbevolking'])}")
        st.write(f"- Bevolking op arbeidsleeftijd: {arbeidsleeftijd} {check(arbeidsleeftijd, referentie['Bevolking op arbeidsleeftijd'])}")

# Kolommen per regio
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🇧🇪 België")
    wl_be = st.number_input("Werklozen", key="wl_be", value=340000, step=1000)
    wn_be = st.number_input("Werkenden", key="wn_be", value=4870000, step=1000)
    na_be = st.number_input("Niet-actieven", key="na_be", value=1300000, step=1000)
    bb_be = wl_be + wn_be
    al_be = bb_be + na_be
    toon_indicatoren("België", wl_be, wn_be, na_be, bb_be, al_be, referentie=officiele)

with col2:
    st.subheader("🟡 Vlaanderen")
    wl_vl = st.number_input("Werklozen", key="wl_vl", value=175000, step=1000)
    wn_vl = st.number_input("Werkenden", key="wn_vl", value=2990000, step=1000)
    na_vl = st.number_input("Niet-actieven", key="na_vl", value=580000, step=1000)
    bb_vl = wl_vl + wn_vl
    al_vl = bb_vl + na_vl
    toon_indicatoren("Vlaanderen", wl_vl, wn_vl, na_vl, bb_vl, al_vl)

with col3:
    st.subheader("🔵 Brussel")
    wl_bru = st.number_input("Werklozen", key="wl_bru", value=95000, step=1000)
    wn_bru = st.number_input("Werkenden", key="wn_bru", value=700000, step=1000)
    na_bru = st.number_input("Niet-actieven", key="na_bru", value=370000, step=1000)
    bb_bru = wl_bru + wn_bru
    al_bru = bb_bru + na_bru
    toon_indicatoren("Brussel", wl_bru, wn_bru, na_bru, bb_bru, al_bru)
