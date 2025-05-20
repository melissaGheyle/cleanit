import streamlit as st

st.set_page_config(page_title="Controle per regio", layout="wide")

st.title("📊 Controle arbeidsmarktindicatoren per regio")
st.markdown("Vergelijk de resultaten voor **België**, **Vlaanderen** en **Brussel**. Vul de aantallen in en controleer of de indicatoren correct berekend zijn.")

def controleblok(regio, beroepsbevolking, arbeidsleeftijd, wlgr_input, actgr_input, wzgr_input):
    st.markdown(f"### 📍 {regio}")

    try:
        werklozen = round(beroepsbevolking * 0.07)  # bijv. 7% werkloosheid (dummy)
        werkenden = beroepsbevolking - werklozen
        niet_actieven = arbeidsleeftijd - beroepsbevolking

        wlgr = round((werklozen / beroepsbevolking) * 100, 1)
        actgr = round((beroepsbevolking / arbeidsleeftijd) * 100, 1)
        wzgr = round((werkenden / arbeidsleeftijd) * 100, 1)
    except ZeroDivisionError:
        wlgr = actgr = wzgr = 0

    st.write(f"- Werklozen: {werklozen}")
    st.write(f"- Werkenden: {werkenden}")
    st.write(f"- Niet-actieven: {niet_actieven}")
    st.write(f"📈 **Berekende waarden:**")
    st.write(f"• Werkloosheidsgraad: {wlgr}%")
    st.write(f"• Activiteitsgraad: {actgr}%")
    st.write(f"• Werkzaamheidsgraad: {wzgr}%")

    fouten = 0

    if wlgr_input == wlgr:
        st.success("✔️ Werkloosheidsgraad correct")
    else:
        st.error(f"❌ Werkloosheidsgraad fout (moet {wlgr}%)")
        fouten += 1

    if actgr_input == actgr:
        st.success("✔️ Activiteitsgraad correct")
    else:
        st.error(f"❌ Activiteitsgraad fout (moet {actgr}%)")
        fouten += 1

    if wzgr_input == wzgr:
        st.success("✔️ Werkzaamheidsgraad correct")
    else:
        st.error(f"❌ Werkzaamheidsgraad fout (moet {wzgr}%)")
        fouten += 1

    if fouten == 0:
        st.balloons()
        st.success("🎉 Proficiat! Alles correct voor deze regio.")

# Maak 3 kolommen naast elkaar
col_be, col_vl, col_bru = st.columns(3)

with col_be:
    st.subheader("🇧🇪 België")
    bb_be = st.number_input("Beroepsbevolking", key="bb_be", value=5210000, step=10000)
    al_be = st.number_input("Arbeidsleeftijd", key="al_be", value=6510000, step=10000)
    wlgr_be = st.number_input("Werkloosheidsgraad (%)", key="wlgr_be", step=0.1)
    actgr_be = st.number_input("Activiteitsgraad (%)", key="actgr_be", step=0.1)
    wzgr_be = st.number_input("Werkzaamheidsgraad (%)", key="wzgr_be", step=0.1)

    if st.button("✅ Controleer België"):
        controleblok("België", bb_be, al_be, wlgr_be, actgr_be, wzgr_be)

with col_vl:
    st.subheader("🟡 Vlaanderen")
    bb_vl = st.number_input("Beroepsbevolking", key="bb_vl", value=3165000, step=10000)
    al_vl = st.number_input("Arbeidsleeftijd", key="al_vl", value=3745000, step=10000)
    wlgr_vl = st.number_input("Werkloosheidsgraad (%)", key="wlgr_vl", step=0.1)
    actgr_vl = st.number_input("Activiteitsgraad (%)", key="actgr_vl", step=0.1)
    wzgr_vl = st.number_input("Werkzaamheidsgraad (%)", key="wzgr_vl", step=0.1)

    if st.button("✅ Controleer Vlaanderen"):
        controleblok("Vlaanderen", bb_vl, al_vl, wlgr_vl, actgr_vl, wzgr_vl)

with col_bru:
    st.subheader("🔵 Brussel")
    bb_bru = st.number_input("Beroepsbevolking", key="bb_bru", value=795000, step=10000)
    al_bru = st.number_input("Arbeidsleeftijd", key="al_bru", value=1165000, step=10000)
    wlgr_bru = st.number_input("Werkloosheidsgraad (%)", key="wlgr_bru", step=0.1)
    actgr_bru = st.number_input("Activiteitsgraad (%)", key="actgr_bru", step=0.1)
    wzgr_bru = st.number_input("Werkzaamheidsgraad (%)", key="wzgr_bru", step=0.1)

    if st.button("✅ Controleer Brussel"):
        controleblok("Brussel", bb_bru, al_bru, wlgr_bru, actgr_bru, wzgr_bru)
