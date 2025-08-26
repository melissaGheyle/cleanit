# 👶 Ouderchatbot – Respijtdagen (Snowflake-native, met NL-kommagetallen)
# Bron: RESPIJT.PUBLIC.RESPIJTDAGEN
# Verwachte kolommen:
#   OPVANG, NAAM_KIND, OPVANGPLAN, BEGINSALDO, OPGEBRUIKT, HUIDIG_SALDO, LAATSTE_UPDATE

import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, upper, lit

# ====== Snowflake objecten ======
DB        = "RESPIJT"
SCHEMA    = "PUBLIC"
TABLE     = "RESPIJTDAGEN"
WAREHOUSE = "ZP_WH"        # pas aan of laat staan; wordt genegeerd als de rol al een WH gebruikt
# =================================

st.set_page_config(page_title="Ouderchatbot – Respijtdagen", page_icon="👶", layout="wide")

# Actieve Snowflake-sessie
session = get_active_session()
session.sql(f"USE DATABASE {DB}").collect()
session.sql(f"USE SCHEMA {SCHEMA}").collect()
try:
    session.sql(f"USE WAREHOUSE {WAREHOUSE}").collect()
except Exception:
    # Warehouse kan al via rol/context gezet zijn
    pass

# ---------- Helpers ----------
def fmt_nl_num(x) -> str:
    """Toon NL getal (komma). Behoud 1 decimaal als die er is; anders geheel getal."""
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    try:
        f = float(x)
    except Exception:
        return str(x)
    if f.is_integer():
        return f"{int(f)}"
    return f"{f:.1f}".replace(".", ",")

@st.cache_data(ttl=300, show_spinner=False)
def list_opvang() -> list[str]:
    df = session.sql(
        f"SELECT DISTINCT OPVANG FROM {DB}.{SCHEMA}.{TABLE} WHERE OPVANG IS NOT NULL ORDER BY 1"
    ).to_pandas()
    return df["OPVANG"].dropna().tolist()

def query_row(opvang: str, naam: str) -> pd.DataFrame:
    """Case-insensitive filter op opvang + naam kind, veilig via Snowpark-functies."""
    df = (
        session.table(f"{DB}.{SCHEMA}.{TABLE}")
        .filter(
            (upper(col("OPVANG")) == upper(lit(opvang))) &
            (upper(col("NAAM_KIND")) == upper(lit(naam)))
        )
        .select(
            "OPVANG", "NAAM_KIND", "OPVANGPLAN",
            "BEGINSALDO", "OPGEBRUIKT", "HUIDIG_SALDO", "LAATSTE_UPDATE"
        )
        .limit(5)
        .to_pandas()
    )
    return df

# ---------------- UI ----------------
st.title("👶 Ouderchatbot – Respijtdagen")
st.caption(f"Bron: {DB}.{SCHEMA}.{TABLE} — draait in Snowflake")

opvangs = list_opvang()
opvang = st.selectbox("🧭 Welke opvang?", options=opvangs or ["— geen data —"])
kind    = st.text_input("🧒 Naam kind (voor- en achternaam)")

if st.button("Toon gegevens"):
    if not opvangs:
        st.error("Geen opvang-lijst beschikbaar (controleer tabel/rechten).")
        st.stop()
    if not kind.strip():
        st.warning("Vul eerst de naam van het kind in.")
        st.stop()

    df = query_row(opvang, kind.strip())
    if df.empty:
        st.info("Geen match gevonden. Controleer spelling/case.")
        st.stop()

    r = df.iloc[0]
    st.success(f"Resultaat voor **{r.get('NAAM_KIND')}** in **{r.get('OPVANG')}**")

    c1, c2, c3 = st.columns(3)
    c1.metric("Beginsaldo respijtdagen",   fmt_nl_num(r.get("BEGINSALDO")))
    c2.metric("Opgebruikte respijtdagen",  fmt_nl_num(r.get("OPGEBRUIKT")))
    c3.metric("Huidig saldo",              fmt_nl_num(r.get("HUIDIG_SALDO")))

    st.markdown(f"**Opvangplan:** {r.get('OPVANGPLAN') or '—'}")
    st.markdown(f"**Laatste update:** {r.get('LAATSTE_UPDATE') or '—'}")

    st.markdown("---")
    st.markdown("**Exacte rij(en) uit Excel**")

    # Voor weergave: kommagetallen tonen in NL-formaat
    df_view = df.copy()
    for kol in ["BEGINSALDO", "OPGEBRUIKT", "HUIDIG_SALDO"]:
        if kol in df_view.columns:
            df_view[kol] = df_view[kol].map(fmt_nl_num)

    st.dataframe(df_view, use_container_width=True)

    # Download: originele (niet-geformatteerde) waarden als CSV
    st.download_button(
        "Download resultaat (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"respijtdagen_{r.get('OPVANG')}_{r.get('NAAM_KIND')}.csv",
        mime="text/csv",
    )
