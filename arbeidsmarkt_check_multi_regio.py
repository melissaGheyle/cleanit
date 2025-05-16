
import streamlit as st

st.set_page_config(page_title="Controle per regio", layout="centered")
st.title("📊 Controle arbeidsmarktindicatoren per regio")

st.markdown("Vergelijk de resultaten voor **België**, **Vlaanderen** en **Brussel**. Vul de aantallen in en controleer of de indicatoren correct berekend zijn.")

def controleblok(regio, werklozen, werkenden, niet_actieven, wlgr_input, actgr_input, wzgr_input):
    st.subheader(f"📍 {regio}")
    beroepsbevolking = werklozen + werkenden
    arbeidsleeftijd = beroepsbevolking + niet_actieven

    try:
        wlgr = round((werklozen / beroepsbevolking) * 100, 1)
        actgr = round((beroepsbevolking / arbeidsleeftijd) * 100, 1)
        wzgr = round((werkenden / arbeidsleeftijd) * 100, 1)
    except ZeroDivisionError:
        wlgr = actgr = wzgr = 0

    st.write(f"Beroepsbevolking: {beroepsbevolking}")
    st.write(f"Bevolking op arbeidsleeftijd: {arbeidsleeftijd}")

    fouten = 0

    if wlgr_input == wlgr:
        st.success(f"✔️ Werkloosheidsgraad klopt: {wlgr}%")
    else:
        st.error(f"❌ Werkloosheidsgraad fout. Correct is {wlgr}%")
        fouten += 1

    if actgr_input == actgr:
        st.success(f"✔️ Activiteitsgraad klopt: {actgr}%")
    else:
        st.error(f"❌ Activiteitsgraad fout. Correct is {actgr}%")
        fouten += 1

    if wzgr_input == wzgr:
        st.success(f"✔️ Werkzaamheidsgraad klopt: {wzgr}%")
    else:
        st.error(f"❌ Werkzaamheidsgraad fout. Correct is {wzgr}%")
        fouten += 1

    if fouten == 0:
        st.balloons()
        st.success("🎉 Proficiat! Alle indicatoren zijn correct berekend.")

# BELGIË
with st.expander("België 2023"):
    wl = st.number_input("Werklozen (BE)", key="wl_be", value=340000, step=1000)
    wn = st.number_input("Werkenden (BE)", key="wn_be", value=4870000, step=1000)
    na = st.number_input("Niet-actieven (BE)", key="na_be", value=1300000, step=1000)
    wlgr = st.number_input("Werkloosheidsgraad (%)", key="wlgr_be", step=0.1)
    actgr = st.number_input("Activiteitsgraad (%)", key="actgr_be", step=0.1)
    wzgr = st.number_input("Werkzaamheidsgraad (%)", key="wzgr_be", step=0.1)

    if st.button("✅ Controleer België"):
        controleblok("België", wl, wn, na, wlgr, actgr, wzgr)

# VLAANDEREN
with st.expander("Vlaanderen 2023"):
    wl = st.number_input("Werklozen (VL)", key="wl_vl", value=175000, step=1000)
    wn = st.number_input("Werkenden (VL)", key="wn_vl", value=2990000, step=1000)
    na = st.number_input("Niet-actieven (VL)", key="na_vl", value=580000, step=1000)
    wlgr = st.number_input("Werkloosheidsgraad (%)", key="wlgr_vl", step=0.1)
    actgr = st.number_input("Activiteitsgraad (%)", key="actgr_vl", step=0.1)
    wzgr = st.number_input("Werkzaamheidsgraad (%)", key="wzgr_vl", step=0.1)

    if st.button("✅ Controleer Vlaanderen"):
        controleblok("Vlaanderen", wl, wn, na, wlgr, actgr, wzgr)

# BRUSSEL
with st.expander("Brussel 2023"):
    wl = st.number_input("Werklozen (BRU)", key="wl_bru", value=95000, step=1000)
    wn = st.number_input("Werkenden (BRU)", key="wn_bru", value=700000, step=1000)
    na = st.number_input("Niet-actieven (BRU)", key="na_bru", value=370000, step=1000)
    wlgr = st.number_input("Werkloosheidsgraad (%)", key="wlgr_bru", step=0.1)
    actgr = st.number_input("Activiteitsgraad (%)", key="actgr_bru", step=0.1)
    wzgr = st.number_input("Werkzaamheidsgraad (%)", key="wzgr_bru", step=0.1)

    if st.button("✅ Controleer Brussel"):
        controleblok("Brussel", wl, wn, na, wlgr, actgr, wzgr)
