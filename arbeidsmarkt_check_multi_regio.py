import streamlit as st

st.set_page_config(page_title="Controle per regio", layout="wide")
st.title("📊 Arbeidsmarktindicatoren per regio")

st.markdown("Vul de vijf gegevens per regio in. Klik op **Controleer invoer** om je antwoorden te vergelijken met de officiële cijfers van 2024.")

# ✅ Officiële cijfers per regio
officieel = {
    "Wallonië": {
        "Werklozen": 129003,
        "Werkenden": 1297081,
        "Niet-actieven": 1048984,
    },
    "Vlaanderen": {
        "Werklozen": 121617,
        "Werkenden": 3090288,
        "Niet-actieven": 1806096,
    },
    "Brussel": {
        "Werklozen": 68380,
        "Werkenden": 512631,
        "Niet-actieven": 361920,
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
    st.subheader(f"🟢 {regio}")
    wl = st.number_input("Werklozen", key=f"{prefix}_wl", value=default[0], step=1000)
    wn = st.number_input("Werkenden", key=f"{prefix}_wn", value=default[1], step=1000)
    na = st.number_input("Niet-actieven", key=f"{prefix}_na", value=default[2], step=1000)
    bb = wl + wn
    al = bb + na

    if wl > 0 and wn > 0 and na > 0:
        wlgr = round((wl / bb) * 100, 1) if bb else 0.0
        actgr = round((bb / al) * 100, 1) if al else 0.0
        wzgr = round((wn / al) * 100, 1) if al else 0.0
    else:
        wlgr = actgr = wzgr = None  # Graden niet tonen

    return {
        "Werklozen": wl, "Werkenden": wn, "Niet-actieven": na,
        "Beroepsbevolking": bb, "Bevolking op arbeidsleeftijd": al,
        "Werkloosheidsgraad": wlgr,
        "Activiteitsgraad": actgr,
        "Werkzaamheidsgraad": wzgr
    }

col1, col2, col3 = st.columns(3)

with col1:
    w_inputs = invoervelden("Wallonië", "w", [130000, 1297000, 1049000])
with col2:
    vl_inputs = invoervelden("Vlaanderen", "vl", [175000, 2990000, 580000])
with col3:
    bru_inputs = invoervelden("Brussel", "bru", [95000, 700000, 370000])

# ✅ Controleknop
if st.button("✅ Controleer invoer"):
    def controle_output(inputs, correct):
        result = {}
        volledig_juist = True
        for key in correct:
            ingevuld = int(inputs[key]) if isinstance(inputs[key], int) else round(inputs[key], 1)
            juist = int(correct[key]) if isinstance(correct[key], int) else round(correct[key], 1)
            if ingevuld == juist:
                result[key] = "✔️"
            else:
                result[key] = f"❌ ({juist})"
                volledig_juist = False
        return result, volledig_juist

    st.markdown("---")
    st.subheader("📋 Controle resultaten per regio")

    w_result, w_ok = controle_output(w_inputs, officieel["Wallonië"])
    vl_result, vl_ok = controle_output(vl_inputs, officieel["Vlaanderen"])
    bru_result, bru_ok = controle_output(bru_inputs, officieel["Brussel"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🟢 Wallonië")
        for key, val in w_result.items():
            if w_inputs[key] is not None:
                st.write(f"- {key}: {w_inputs[key]} {val}")
    with col2:
        st.markdown("### 🟡 Vlaanderen")
        for key, val in vl_result.items():
            if vl_inputs[key] is not None:
                st.write(f"- {key}: {vl_inputs[key]} {val}")
    with col3:
        st.markdown("### 🔵 Brussel")
        for key, val in bru_result.items():
            if bru_inputs[key] is not None:
                st.write(f"- {key}: {bru_inputs[key]} {val}")

    alles_correct = w_ok and vl_ok and bru_ok

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
        st.info("📌 Tip: enkel als alle gegevens correct zijn ingevuld wordt de vergelijking per indicator getoond.")
