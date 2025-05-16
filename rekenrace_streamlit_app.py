import streamlit as st

st.set_page_config(page_title="Rekenrace", layout="centered")

st.title("🎯 Rekenrace – Arbeidsmarktindicatoren")

st.markdown("Voer de juiste waarden in om de indicatoren te berekenen. Veel succes!")

# Gegeven blokken
st.markdown("### Gegeven blokken")
st.info("🔵 Werklozen: **6** | 🟢 Werkenden: **24** | ⚪ Niet-actieven: **10**")

# Invoer door leerling
st.markdown("### Jouw antwoorden")

bb = st.number_input("1️⃣ Beroepsbevolking", min_value=0, step=1)
al = st.number_input("2️⃣ Bevolking op arbeidsleeftijd", min_value=0, step=1)
wlgr = st.number_input("3️⃣ Werkloosheidsgraad (%)", min_value=0.0, step=0.1)
actgr = st.number_input("4️⃣ Activiteitsgraad (%)", min_value=0.0, step=0.1)
wzgr = st.number_input("5️⃣ Werkzaamheidsgraad (%)", min_value=0.0, step=0.1)

# Correcte waarden
correcte_bb = 6 + 24
correcte_al = correcte_bb + 10
correcte_wlgr = round((6 / correcte_bb) * 100, 1)
correcte_actgr = round((correcte_bb / correcte_al) * 100, 1)
correcte_wzgr = round((24 / correcte_al) * 100, 1)

if st.button("✅ Controleer"):
    score = 0

    if bb == correcte_bb:
        st.success("✅ Beroepsbevolking is correct!")
        score += 1
    else:
        st.error(f"❌ Beroepsbevolking is fout. Correct: {correcte_bb}")

    if al == correcte_al:
        st.success("✅ Bevolking op arbeidsleeftijd is correct!")
        score += 1
    else:
        st.error(f"❌ Arbeidsleeftijd is fout. Correct: {correcte_al}")

    if round(wlgr, 1) == correcte_wlgr:
        st.success("🎯 Werkloosheidsgraad is correct!")
        score += 1
    else:
        st.error(f"❌ Werkloosheidsgraad fout. Correct: {correcte_wlgr}%")

    if round(actgr, 1) == correcte_actgr:
        st.success("🎯 Activiteitsgraad is correct!")
        score += 1
    else:
        st.error(f"❌ Activiteitsgraad fout. Correct: {correcte_actgr}%")

    if round(wzgr, 1) == correcte_wzgr:
        st.success("🎯 Werkzaamheidsgraad is correct!")
        score += 1
    else:
        st.error(f"❌ Werkzaamheidsgraad fout. Correct: {correcte_wzgr}%")

    if score == 5:
        st.balloons()
        st.success("🏆 Fantastisch! Alles correct!")
    else:
        st.info(f"Je had {score}/5 juist.")

# Formules
with st.expander("📘 Toon de formules"):
    st.code("""
Beroepsbevolking = werklozen + werkenden
Bevolking op arbeidsleeftijd = werklozen + werkenden + niet-actieven
Werkloosheidsgraad = (werklozen / beroepsbevolking) × 100
Activiteitsgraad = (beroepsbevolking / bevolking op arbeidsleeftijd) × 100
Werkzaamheidsgraad = (werkenden / bevolking op arbeidsleeftijd) × 100
    """, language="text")
