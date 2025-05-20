import streamlit as st

st.set_page_config(page_title="Controle per regio", layout="wide")

st.title("📊 Arbeidsmarktindicatoren per regio")
st.markdown("Voer de vijf basisgegevens in voor elke regio. De indicatoren worden automatisch berekend op basis van jouw invoer.")

def toon_indicatoren(regio, werklozen, werkenden, niet_actieven, beroepsbevolking, arbeidsleeftijd):
    st.markdown(f"### 📍 {regio}")

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

# 3 kolommen naast elkaar
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🇧🇪 België")
    wl_be = st.number_input("Werklozen", key="wl_be", value=340000, step=1000)
    wn_be = st.number_input("Werkenden", key="wn_be", value=4870000, step=1000)
    na_be = st.number_input("Niet-actieven", key="na_be", value=1300000, step=1000)
    bb_be = st.number_input("Beroepsbevolking", key="bb_be", value=5210000, step=1000)
    al_be = st.number_input("Bevolking op arbeidsleeftijd", key="al_be", value=6510000, step=1000)
    toon_indicatoren("België", wl_be, wn_be, na_be, bb_be, al_be)

with col2:
    st.subheader("🟡 Vlaanderen")
    wl_vl = st.number_input("Werklozen", key="wl_vl", value=175000, step=1000)
    wn_vl = st.number_input("Werkenden", key="wn_vl", value=2990000, step=1000)
    na_vl = st.number_input("Niet-actieven", key="na_vl", value=580000, step=100_
