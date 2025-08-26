# 👶 Ouderchatbot – Respijtdagen (Excel, géén Snowflake)
# - Leest respijtdagen.xlsx (lokaal in repo) of via Upload
# - Zoekt op Opvang + Naam kind (case-insensitive)
# - Metrics met NL-kommagetallen
# - Toont exacte rij(en) en biedt CSV-download

import io
import re
from pathlib import Path
import pandas as pd
import streamlit as st

EXCEL_FILE = "respijtdagen.xlsx"   # zet je bestand in de repo met deze naam

st.set_page_config(page_title="Ouderchatbot – Respijtdagen (Excel)", page_icon="👶", layout="wide")
st.title("👶 Ouderchatbot – Respijtdagen")
st.caption("Bron: Excel-bestand (alle tabs/sheets worden ingelezen)")

# ---------- helpers ----------
def fmt_nl_num(x) -> str:
    """Toon NL getal (komma). 0 decimalen als het exact geheel is, anders 1 decimaal."""
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    try:
        f = float(x)
    except Exception:
        # als het bv. '8,5' als string is: vervang komma en probeer opnieuw
        try:
            f = float(str(x).replace(",", "."))
        except Exception:
            return str(x)
    if f.is_integer():
        return f"{int(f)}"
    return f"{f:.1f}".replace(".", ",")

def _norm(s: str) -> str:
    """normalizeer kolomnamen voor robuuste mapping."""
    s = (s or "").strip().lower()
    s = s.replace("\xa0", " ")
    s = re.sub(r"[\s_-]+", " ", s)
    return s

def _map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """hernoem kolommen van de sheet naar vaste namen."""
    colmap = {}
    for c in df.columns:
        k = _norm(str(c))
        if k in ("opvang",):
            colmap[c] = "opvang"
        elif k in ("naam kind", "naam_kind", "naamkind", "kind", "naam"):
            colmap[c] = "naam_kind"
        elif k in ("opvangplan", "plan", "opvang plan"):
            colmap[c] = "opvangplan"
        elif k in ("beginsaldo", "beginsaldo respijtdagen", "startsaldo"):
            colmap[c] = "beginsaldo"
        elif k in ("opgebruikte respijtdagen", "opgenomen dagen", "opgebruikt", "opgebruikte dagen"):
            colmap[c] = "opgebruikt"
        elif k in ("huidig saldo", "huidig_saldo", "saldo"):
            colmap[c] = "huidig_saldo"
        elif k in ("laatste update", "laatste_update", "update", "datum", "datum update"):
            colmap[c] = "laatste_update"
        else:
            # laat onbekende kolommen zoals ze zijn
            colmap[c] = c
    return df.rename(columns=colmap)

def _to_float(series: pd.Series) -> pd.Series:
    """converteer strings als '16,5' of '16.5' naar float."""
    return pd.to_numeric(
        series.astype(str).str.replace("\xa0", "", regex=False).str.replace(" ", "", regex=False).str.replace(",", ".", regex=False),
        errors="coerce"
    )

@st.cache_data(show_spinner=False)
def load_all_sheets_any(io_or_path) -> pd.DataFrame:
    """Lees alle sheets; voeg kolommen 'Sheet' en 'ExcelRij' toe; normaliseer kolomnamen."""
    xls = pd.read_excel(io_or_path, sheet_name=None, dtype=str)  # alles als tekst inlezen
    frames = []
    for sheet, df in xls.items():
        if df is None or df.empty:
            continue
        df = df.copy()
        df = _map_columns(df)
        # Excel-rij (header is rij 1): index (0-based) + 2
        df["Sheet"] = sheet
        df["ExcelRij"] = (df.reset_index().index + 2).astype(str)

        # Numeriek maken waar relevant (na mappen)
        for kol in ("beginsaldo", "opgebruikt", "huidig_saldo"):
            if kol in df.columns:
                df[kol] = _to_float(df[kol])

        frames.append(df)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)

# ---------- data-bron ----------
with st.sidebar:
    st.markdown("### 📄 Excel laden")
    uploaded = st.file_uploader("Upload een nieuw Excel-bestand", type=["xlsx"])
    st.caption("Als je niets uploadt, wordt het bestand in de repo gebruikt: `respijtdagen.xlsx`.")

# bron kiezen
if uploaded:
    df_all = load_all_sheets_any(uploaded)
else:
    if not Path(EXCEL_FILE).exists():
        st.error(f"Bestand niet gevonden: `{EXCEL_FILE}`. Upload een Excel in de sidebar of voeg het toe aan je repo.")
        st.stop()
    df_all = load_all_sheets_any(EXCEL_FILE)

if df_all.empty:
    st.warning("Geen gegevens gevonden in het Excel-bestand.")
    st.stop()

# --------- UI: selectie ---------
opvangs = sorted([v for v in df_all.get("opvang", pd.Series()).dropna().unique()])
opvang = st.selectbox("🎯 Welke opvang?", options=opvangs or ["— geen data —"])
kind   = st.text_input("🧒 Naam kind (voor- en achternaam)", placeholder="bv. Thio Demaj")

# --------- Zoeken & tonen ---------
def _ci(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.casefold()

if st.button("Toon gegevens"):
    if not opvangs:
        st.error("Geen opvang-waarden gevonden in Excel.")
        st.stop()
    if not kind.strip():
        st.warning("Vul eerst de naam van het kind in.")
        st.stop()

    mask = (_ci(df_all["opvang"]) == opvang.strip().casefold()) & (_ci(df_all["naam_kind"]) == kind.strip().casefold())
    df = df_all.loc[mask].copy()

    if df.empty:
        st.info("Geen match gevonden. Controleer spelling/case of kies de juiste opvang.")
        st.stop()

    # Toon eerste match als metrics
    r = df.iloc[0]

    st.success(f"Resultaat voor **{r.get('naam_kind', '')}** in **{r.get('opvang', '')}**")

    c1, c2, c3 = st.columns(3)
    c1.metric("Beginsaldo respijtdagen",   fmt_nl_num(r.get("beginsaldo")))
    c2.metric("Opgebruikte respijtdagen", fmt_nl_num(r.get("opgebruikt")))
    c3.metric("Huidig saldo",             fmt_nl_num(r.get("huidig_saldo")))

    st.markdown(f"**Opvangplan:** {r.get('opvangplan', '—') or '—'}")
    st.markdown(f"**Laatste update:** {r.get('laatste_update', '—') or '—'}")

    st.markdown("---")
    st.markdown("**Exacte rij(en) uit Excel**")

    # Voor weergave: kommagetallen zetten met NL-notatie
    view = df.copy()
    for kol in ("beginsaldo", "opgebruikt", "huidig_saldo"):
        if kol in view.columns:
            view[kol] = view[kol].map(fmt_nl_num)

    # kolommen iets netter ordenen als ze bestaan
    pref_order = [k for k in ["Sheet","ExcelRij","opvang","naam_kind","opvangplan","beginsaldo","opgebruikt","huidig_saldo","laatste_update"] if k in view.columns]
    other_cols = [c for c in view.columns if c not in pref_order]
    view = view[pref_order + other_cols]

    st.dataframe(view, use_container_width=True)

    st.download_button(
        "Download resultaat (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"respijtdagen_{r.get('opvang','')}_{r.get('naam_kind','')}.csv",
        mime="text/csv",
    )
