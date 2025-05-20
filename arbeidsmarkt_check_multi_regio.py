import streamlit as st

st.set_page_config(page_title="Controle per regio", layout="wide")

st.title("📊 Arbeidsmarktindicatoren per regio")
st.markdown("Vul de beroepsbevolking en bevolking op arbeidsleeftijd in om automatisch de indicatoren te berekenen voor **België**, **Vlaanderen** en **Brussel**.")

def toon_indicatoren(regio, bb, al):
    st.markdown(f"### 📍 {regio}")

    # Simulatie: stel 7% werkloosheid voor demo
    werklozen = round(bb * 0.07)
    werkenden = bb - werklozen
    niet_actieven = al - bb

    try:
        wlgr = round((werklozen / bb) * 100, 1)
        actgr = round((bb / al) * 100, 1)
        wzgr = round((werkenden / al) * 100, 1)
    except ZeroDivisionError:
        wlgr = actgr = wzgr = 0

    st.write(f"👥 **Werklozen**: {werklozen}")
    st.write(f"👷 **Werkenden**: {werkenden}")
    st.write(f"🚫 **Niet-actieven**: {niet_actieven}")
    st.markdown("---")
    st.metric(label="📉 Werkloosheidsgraad", value=f"{wlgr} %")
    st.metric(label="📊 Activiteitsgraad", value=f"{actgr} %")
    st.metric(label="💼 Werkzaamheidsgraad", value=f"{wzgr} %")

# Layout in 3 kolommen
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🇧🇪 België")
    bb_be = st.number_input("Beroepsbevolking", key="bb_be", value=5210000, step=10000)
    al_be = st.number_input("Arbeidsleeftijd", key="al_be", value=6510000, step=10000)
    toon_indicatoren("België", bb_be, al_be)

with col2:
    st.subheader("🟡 Vlaanderen")
    bb_vl = st.number_input("Beroepsbevolking", key="bb_vl", value=3165000, step=10000)
    al_vl = st.number_input("Arbeidsleeftijd", key="al_vl", value=3745000, step=10000)
    toon_indicatoren("Vlaanderen", bb_vl, al_vl)

with col3:
    st.subheader("🔵 Brussel")
    bb_bru = st.number_input("Beroepsbevolking", key="bb_bru", value=795000, step=10000)
    al_bru = st.number_input("Arbeidsleeftijd", key="al_bru", value=1165000, step=10000)
    toon_indicatoren("Brussel", bb_bru, al_bru)
