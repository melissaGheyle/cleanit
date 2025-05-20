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

# Bereken afgeleide cijfers
for regio in officieel:
    data = officieel[regio]
    data["Beroepsbevolking"] = data["Werklozen"] + data["Werkenden"]
    data["Bevolking op arbeidsleeftijd"] = data["Beroepsbevolking"] + data["Niet-actieven"]

# 📥 Invoer door gebruiker
def invoervelden(regio, prefix, default):
    st.subheader(f"📍 {regio}")
    wl = st.number_input("Werklozen", key=f"{prefix}_wl", value=default[0], step=1000)
    wn = st.number_input("Werkenden", key=f"{prefix}_wn", value=default[1], step=1000)
    na = st.number_input("Niet-actieven", key=f"{prefix}_na", value=default[2], step=1000)
    bb = wl + wn
    al = bb + na
    return {"Werklozen": wl, "Werkenden": wn, "Niet-actieven": na, "Beroepsbevolking": bb, "Bevolking op arbeidsleeftijd": al}

col1, col2, col3 = st.columns(3)

with col1:
    be_inputs = invoervelden("🇧🇪 België", "be", [340000, 4870000, 1300000])
with col2:
    vl_inputs = invoervelden("🟡 Vlaanderen", "vl", [175000, 2990000, 580000])
with col3:
    bru_inputs = invoervelden("🔵 Brussel", "bru", [95000, 700000, 370000])

# 🟢 Toon controle na knopdruk
if st.button("✅ Controleer invoer"):
    def controle_output(inputs, correct):
        result = {}
        for key in correct:
            ingevuld = int(inputs[key])
            juist = correct[key]
            result[key] = "✔️" if ingevuld == juist else f"❌ ({juist})"
        return result

    st.markdown("---")
    st.subheader("📋 Resultaat van de controle")

    be_result = controle_output(be_inputs, officieel["België"])
    vl_result = controle_output(vl_inputs, officieel["Vlaanderen"])
    bru_result = controle_output(bru_inputs, officieel["Brussel"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🇧🇪 België")
        for key, val in be_result.items():
            st.write(f"- {key}: {int(be_inputs[key])} {val}")
    with col2:
        st.markdown("### 🟡 Vlaanderen")
        for key, val in vl_result.items():
            st.write(f"- {key}: {int(vl_inputs[key])} {val}")
    with col3:
        st.markdown("### 🔵 Brussel")
        for key, val in bru_result.items():
            st.write(f"- {key}: {int(bru_inputs[key])} {val}")
