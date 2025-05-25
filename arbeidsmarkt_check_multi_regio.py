import streamlit as st

# 📊 Pagina-instellingen
st.set_page_config(page_title="Controle per regio", layout="wide")
st.title("📊 Arbeidsmarktindicatoren per regio")

st.markdown(
    "Vul de drie kerncijfers per regio in. Klik op **Controleer invoer** om je antwoorden te vergelijken met de officiële cijfers van 2024."
)

# ✅ Officiële cijfers per regio
officieel = {
    "Wallonië": {"Werklozen": 116182, "Werkenden": 1453396, "Niet-actieven": 1167783},
    "Vlaanderen": {"Werklozen": 121617, "Werkenden": 3090288, "Niet-actieven": 1806096},
    "Brussel": {"Werklozen": 68380, "Werkenden": 512631, "Niet-actieven": 361920},
}

# 🔁 Bereken afgeleide cijfers + indicatoren
def bereken_indicatoren(data):
    wl = data["Werklozen"]
    wn = data["Werkenden"]
    na = data["Niet-actieven"]
    bb = wl + wn
    al = bb + na
    data["Beroepsbevolking"] = bb
    data["Bevolking op arbeidsleeftijd"] = al
    data["Werkloosheidsgraad"] = round((wl / bb) * 100, 1) if bb else 0.0
    data["Activiteitsgraad"] = round((bb / al) * 100, 1) if al else 0.0
    data["Werkzaamheidsgraad"] = round((wn / al) * 100, 1) if al else 0.0

for regio in officieel:
    bereken_indicatoren(officieel[regio])

# 📥 Invoervelden
def invoervelden(regio, prefix, default, emoji):
    st.subheader(f"{emoji} {regio}")
    wl = st.number_input("Werklozen", key=f"{prefix}_wl", value=default["Werklozen"], step=1000)
    wn = st.number_input("Werkenden", key=f"{prefix}_wn", value=default["Werkenden"], step=1000)
    na = st.number_input("Niet-actieven", key=f"{prefix}_na", value=default["Niet-actieven"], step=1000)

    bb = wl + wn
    al = bb + na

    wlgr = round((wl / bb) * 100, 1) if bb else 0.0
    actgr = round((bb / al) * 100, 1) if al else 0.0
    wzgr = round((wn / al) * 100, 1) if al else 0.0

    return {
        "Werklozen": wl,
        "Werkenden": wn,
        "Niet-actieven": na,
        "Beroepsbevolking": bb,
        "Bevolking op arbeidsleeftijd": al,
        "Werkloosheidsgraad": wlgr,
        "Activiteitsgraad": actgr,
        "Werkzaamheidsgraad": wzgr,
    }

# 📊 Invoer per regio
col1, col2, col3 = st.columns(3)
with col1:
    w_inputs = invoervelden("Wallonië", "w", officieel["Wallonië"], "🟢")
with col2:
    vl_inputs = invoervelden("Vlaanderen", "vl", officieel["Vlaanderen"], "🟡")
with col3:
    bru_inputs = invoervelden("Brussel", "bru", officieel["Brussel"], "🔵")

# ✅ Controleknop
if st.button("✅ Controleer invoer"):
    def controle_output(user_inputs, correct_data):
        result = {}
        volledig_juist = True
        for key in correct_data:
            user_value = round(user_inputs.get(key, 0), 1)
            correct_value = round(correct_data[key], 1)
            if user_value == correct_value:
                result[key] = "✔️"
            else:
                result[key] = f"❌ ({correct_value})"
                volledig_juist = False
        return result, volledig_juist

    # 🎯 Resultaten per regio
    st.markdown("---")
    st.subheader("📋 Controle resultaten per regio")

    w_result, w_ok = controle_output(w_inputs, officieel["Wallonië"])
    vl_result, vl_ok = controle_output(vl_inputs, officieel["Vlaanderen"])
    bru_result, bru_ok = controle_output(bru_inputs, officieel["Brussel"])

    for col, regio, result, data in zip(
        st.columns(3),
        ["🟢 Wallonië", "🟡 Vlaanderen", "🔵 Brussel"],
        [w_result, vl_result, bru_result],
        [w_inputs, vl_inputs, bru_inputs],
    ):
        with col:
            st.markdown(f"### {regio}")
            for key, val in result.items():
                st.write(f"- {key}: {data[key]} {val}")

    alles_correct = w_ok and vl_ok and bru_ok

    # 🏆 Hoogste scores
    if alles_correct:
        st.markdown("---")
        st.subheader("🏆 Hoogste score per indicator (alleen zichtbaar bij correcte invoer)")

        hoogste = {
            "Werkloosheidsgraad": max(officieel.items(), key=lambda x: x[1]["Werkloosheidsgraad"]),
            "Activiteitsgraad": max(officieel.items(), key=lambda x: x[1]["Activiteitsgraad"]),
            "Werkzaamheidsgraad": max(officieel.items(), key=lambda x: x[1]["Werkzaamheidsgraad"]),
        }

        st.markdown(f"- 📉 **Hoogste werkloosheidsgraad**: **{hoogste['Werkloosheidsgraad'][0]}** ({hoogste['Werkloosheidsgraad'][1]['Werkloosheidsgraad']}%)")
        st.markdown(f"- 📊 **Hoogste activiteitsgraad**: **{hoogste['Activiteitsgraad'][0]}** ({hoogste['Activiteitsgraad'][1]['Activiteitsgraad']}%)")
        st.markdown(f"- 💼 **Hoogste werkzaamheidsgraad**: **{hoogste['Werkzaamheidsgraad'][0]}** ({hoogste['Werkzaamheidsgraad'][1]['Werkzaamheidsgraad']}%)")
    else:
        st.info("📌 Tip: enkel als alle cijfers correct zijn ingevuld, worden de vergelijkingen per indicator getoond.")
