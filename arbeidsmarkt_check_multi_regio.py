import streamlit as st

st.set_page_config(page_title="Controle per regio", layout="wide")
st.title("📊 Arbeidsmarktindicatoren per regio")

st.markdown("Vul de vijf gegevens per regio in. Klik vervolgens op **Controleer invoer** om na te gaan of je waarden kloppen met de officiële cijfers van 2023.")

# ✅ Officiële cijfers per regio
officieel = {
    "België": {
        "Werklozen": 306179,
        "Werkenden": 5056315,
        "Niet-actieven": 3335799,
    },
    "Vlaanderen": {
        "Werklozen": 119469,
        "Werkenden": 4677292,
        "Niet-actieven": 1177859,
    },
    "Brussel": {
        "Werklozen": 186710,
        "Werkenden": 379023,
        "Niet-actieven": 2157940,
    }
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

# 📥 Invoer door gebruiker
def invoervelden(regio, prefix, default):
    st.subheader(f"📍 {regio}")
    wl = st.number_input("Werklozen", key=f"{prefix}_wl", value=default[0], step=1000)
    wn = st.number_input("Werkenden", key=f"{prefix}_wn", value=default[1], step=1000)
    na = st.number_input("Niet-actieven", key=f"{prefix}_na", value=default[2], step=1000)
    bb = wl + wn
    al = bb + na
    wlgr = round((wl / bb) * 100, 1) if bb else 0.0
    actgr = round((bb / al) * 100, 1) if al else 0.0
    wzgr = round((wn / al) * 100, 1) if al else 0.0
    return {
        "Werklozen": wl, "Werkenden": wn, "Niet-actieven": na,
        "Beroepsbevolking": bb, "Bevolking op arbeidsleeftijd": al,
        "Werkloosheidsgraad": wlgr,
        "Activiteitsgraad": actgr,
        "Werkzaamheidsgraad": wzgr
    }

col1, col2, col3 = st.columns(3)

with col1:
    be_inputs = invoervelden("🇧🇪 België", "be", [340000, 4870000, 1300000])
with col2:
    vl_inputs = invoervelden("🟡 Vlaanderen", "vl", [175000, 2990000, 580000])
with col3:
    bru_inputs = invoervelden("🔵 Brussel", "bru", [95000, 700000, 370000])

# ✅ Controleknop
if st.button("✅ Controleer invoer"):
    def controle_output(inputs, correct):
        result = {}
        for key in correct:
            ingevuld = int(inputs[key]) if isinstance(inputs[key], int) else round(inputs[key], 1)
            juist = int(correct[key]) if isinstance(correct[key], int) else round(correct[key], 1)
            result[key] = "✔️" if ingevuld == juist else f"❌ ({juist})"
        return result

    st.markdown("---")
    st.subheader("📋 Controle resultaten per regio")

    be_result = controle_output(be_inputs, officieel["België"])
    vl_result = controle_output(vl_inputs, officieel["Vlaanderen"])
    bru_result = controle_output(bru_inputs, officieel["Brussel"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🇧🇪 België")
        for key in be_result:
            st.write(f"- {key}: {be_inputs[key]} {be_result[key]}")
    with col2:
        st.markdown("### 🟡 Vlaanderen")
        for key in vl_result:
            st.write(f"- {key}: {vl_inputs[key]} {vl_result[key]}")
    with col3:
        st.markdown("### 🔵 Brussel")
        for key in bru_result:
            st.write(f"- {key}: {bru_inputs[key]} {bru_result[key]}")

    # 📊 Highlight hoogste indicatorwaarden
    st.markdown("---")
    st.subheader("🏆 Hoogste score per indicator")

    hoogste = {
        "Werkloosheidsgraad": max(officieel.items(), key=lambda x: x[1]["Werkloosheidsgraad"]),
        "Activiteitsgraad": max(officieel.items(), key=lambda x: x[1]["Activiteitsgraad"]),
        "Werkzaamheidsgraad": max(officieel.items(), key=lambda x: x[1]["Werkzaamheidsgraad"]),
    }

    st.markdown(f"- 📉 **Hoogste werkloosheidsgraad**: **{hoogste['Werkloosheidsgraad'][0]}** ({hoogste['Werkloosheidsgraad'][1]['Werkloosheidsgraad']}%)")
    st.markdown(f"- 📊 **Hoogste activiteitsgraad**: **{hoogste['Activiteitsgraad'][0]}** ({hoogste['Activiteitsgraad'][1]['Activiteitsgraad']}%)")
    st.markdown(f"- 💼 **Hoogste werkzaamheidsgraad**: **{hoogste['Werkzaamheidsgraad'][0]}** ({hoogste['Werkzaamheidsgraad'][1]['Werkzaamheidsgraad']}%)")
