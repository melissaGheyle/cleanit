import streamlit as st
import random

# Woordenlijst
woordenlijst = ["streamlit", "melissa", "appeltaart", "zorgpunt", "python", "galgje", "rekenen"]

# Initialisatie bij opstart
if "geheim" not in st.session_state:
    st.session_state.geheim = random.choice(woordenlijst)
    st.session_state.geraden = []
    st.session_state.fouten = 0
    st.session_state.einde = False
    st.session_state.gewonnen = False
    st.session_state.feedback = ""

geheim = st.session_state.geheim
geraden = st.session_state.geraden
fouten = st.session_state.fouten
max_fouten = 6

st.title("🎯 Galgje – Raad het Woord!")

# Input voor letter
if not st.session_state.einde:
    letter = st.text_input("Raad een letter:", max_chars=1).lower()

    if st.button("Check"):
        if not letter or not letter.isalpha():
            st.session_state.feedback = "⚠️ Geef een geldige letter in."
        elif letter in geraden:
            st.session_state.feedback = f"ℹ️ Je had '{letter}' al geprobeerd."
        elif letter in geheim:
            geraden.append(letter)
            st.session_state.feedback = f"✅ Goed! De letter '{letter}' zit in het woord."
        else:
            st.session_state.fouten += 1
            geraden.append(letter)
            st.session_state.feedback = f"❌ Jammer, de letter '{letter}' zit er niet in."

# Woordmasker tonen (live)
woord_masker = " ".join([l if l in geraden else "_" for l in geheim])
st.subheader(woord_masker)

# Feedback
if st.session_state.feedback:
    st.info(st.session_state.feedback)

# Check spelstatus
if "_" not in woord_masker.replace(" ", ""):
    st.session_state.einde = True
    st.session_state.gewonnen = True
    st.success("🎉 Proficiat! Je hebt het woord geraden!")
    st.balloons()
elif fouten >= max_fouten:
    st.session_state.einde = True
    st.error("💀 Je hebt verloren.")
    st.info(f"Het juiste woord was: **{geheim}**")

# Pogingen
st.write(f"❌ Fouten: {fouten} / {max_fouten}")

# Nieuw spel starten
if st.session_state.einde:
    if st.button("🔁 Nieuw spel"):
        st.session_state.clear()
        st.rerun()
