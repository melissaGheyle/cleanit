# 👶 Ouderchatbot – Respijtdagen (opvang + vrije invoer naam kind)
# - Leest alle tabs uit respijtdagen.xlsx (eerste rij = kolomnamen)
# - Stap 1: kies opvang
# - Stap 2: tik naam kind (vrije tekst, met suggesties)
# - Antwoord: exacte rij (of best passende) + kernwaarden + downloadknop

from pathlib import Path
import re
from typing import List, Optional

import pandas as pd
import streamlit as st
from difflib import get_close_matches

st.set_page_config(page_title="Ouderchatbot – Respijtdagen", page_icon="👶", layout="wide")
EXCEL_FILE = "respijtdagen.xlsx"   # Plaats dit bestand naast dit script

# ---------------- Helpers ----------------
def load_all_sheets(path: Path) -> pd.DataFrame:
    """Lees alle sheets en concateneer; voeg 'Sheet' en 'ExcelRij' toe (header=rij1)."""
    xls = pd.read_excel(path, sheet_name=None, dtype=str)  # openpyxl voor .xlsx
    frames = []
    for sheet, df in xls.items():
        if df is None or df.empty:
            continue
        df = df.copy()
        df.columns = [str(c).strip() for c in df.columns]
        df = df.fillna("")
        df.insert(0, "Sheet", sheet)
        df["ExcelRij"] = (df.reset_index().index + 2).astype(str)  # +2: header + 1-based
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip()).casefold()

def parse_number(x) -> Optional[float]:
    if x is None or str(x).strip() == "":
        return None
    s = str(x).replace(",", ".")
    m = re.search(r"(-?\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None

def find_col(cols: List[str], targets: List[str]) -> Optional[str]:
    """Zoek kolom op basis van (bijna) naam; eerst exacte, dan bevat-match."""
    lower = {c.lower(): c for c in cols}
    for t in targets:
        if t.lower() in lower:
            return lower[t.lower()]
    scored = []
    for c in cols:
        score = sum(t in c.lower() for t in targets)
        scored.append((score, c))
    scored.sort(reverse=True)
    return scored[0][1] if scored and scored[0][0] > 0 else None

# ---------------- UI ----------------
st.title("👶 Ouderchatbot – Respijtdagen")
st.caption("Kies **opvang** en tik **naam kind**. De bot toont de **exacte rij** uit de Excel + kernwaarden.")

p = Path(EXCEL_FILE)
if not p.exists():
    st.error(f"Bestand niet gevonden: {p.resolve()}")
    st.stop()

df_all = load_all_sheets(p)
if df_all.empty:
    st.error("Het Excelbestand lijkt leeg te zijn.")
    st.stop()

cols = list(df_all.columns)

# Kolommen zoals in je voorbeeld (case-insensitive + handmatig aanpasbaar)
col_opvang   = find_col(cols, ["opvang"])
col_kind     = find_col(cols, ["naam kind", "kind"])
col_plan     = find_col(cols, ["opvangplan"])
col_begin    = find_col(cols, ["beginsaldo respijtdagen", "beginsaldo"])
col_gebruikt = find_col(cols, ["opgebruikte respijtdagen", "opgebruikt", "gebruikt"])
col_saldo    = find_col(cols, ["huidig saldo", "saldo"])
col_update   = find_col(cols, ["laatste update", "update", "datum"])

with st.sidebar:
    st.subheader("📄 Ingeladen bestand")
    st.write(f"• {EXCEL_FILE}")
    st.markdown("---")
    st.caption("Gevonden kolommen (pas aan indien labels afwijken):")
    col_opvang   = st.selectbox("Kolom: opvang", options=cols, index=cols.index(col_opvang) if col_opvang in cols else 0)
    col_kind     = st.selectbox("Kolom: naam kind", options=cols, index=cols.index(col_kind) if col_kind in cols else 1)
    col_plan     = st.selectbox("Kolom: opvangplan", options=cols, index=cols.index(col_plan) if col_plan in cols else 2)
    col_begin    = st.selectbox("Kolom: beginsaldo respijtdagen", options=cols, index=cols.index(col_begin) if col_begin in cols else 3)
    col_gebruikt = st.selectbox("Kolom: opgebruikte respijtdagen", options=cols, index=cols.index(col_gebruikt) if col_gebruikt in cols else 4)
    col_saldo    = st.selectbox("Kolom: huidig saldo", options=cols, index=cols.index(col_saldo) if col_saldo in cols else 5)
    col_update   = st.selectbox("Kolom: laatste update", options=cols, index=cols.index(col_update) if col_update in cols else 6)

# 1) Kies opvang
opvangs = sorted([v for v in df_all[col_opvang].unique() if str(v).strip()])
opvang = st.selectbox("🧭 Welke opvang?", options=opvangs)

# 2) Vrij invulveld voor naam kind (met suggesties)
subset = df_all[df_all[col_opvang].astype(str).str.strip().str.casefold() == str(opvang).strip().casefold()]
kids = sorted([v for v in subset[col_kind].unique() if str(v).strip()])
kind_input = st.text_input("🧒 Naam kind (voor- en achternaam)", placeholder="bv. Florence Carlier")

# Suggesties (niet klikbaar, ter hint bij tikfouten)
if kind_input.strip():
    sugg = get_close_matches(kind_input.strip(), kids, n=5, cutoff=0.6)
    if sugg and kind_input.strip().casefold() not in [k.casefold() for k in kids]:
        st.caption("Bedoelde je: " + " · ".join(sugg))

# Actie
if st.button("Toon gegevens"):
    if not kind_input.strip():
        st.warning("Vul eerst de naam van het kind in.")
        st.stop()

    # 1) Exacte (case-insensitive) match
    rows = subset[subset[col_kind].astype(str).map(lambda x: normalize(x) == normalize(kind_input))]

    # 2) Fallback: dichtstbijzijnde suggestie (alleen als geen exact)
    used_suggestion = False
    if rows.empty:
        close = get_close_matches(kind_input.strip(), kids, n=1, cutoff=0.7)
        if close:
            rows = subset[subset[col_kind].astype(str).map(lambda x: normalize(x) == normalize(close[0]))]
            used_suggestion = not rows.empty

    if rows.empty:
        st.info("Geen rij gevonden voor deze keuze (opvang + naam kind).")
        st.stop()

    first = rows.iloc[0]
    beginsaldo = parse_number(first.get(col_begin))
    gebruikt   = parse_number(first.get(col_gebruikt))
    saldo      = parse_number(first.get(col_saldo))
    update     = str(first.get(col_update) or "").strip()
    plan       = str(first.get(col_plan) or "").strip()

    title = f"Resultaat voor **{first[col_kind]}** in **{opvang}**"
    if used_suggestion:
        title += "  _(beste match op ingevoerde naam)_"
    st.success(title)

    c1, c2, c3 = st.columns(3)
    c1.metric("Beginsaldo respijtdagen", f"{int(beginsaldo):d}" if beginsaldo is not None else "—")
    c2.metric("Opgebruikte respijtdagen", f"{int(gebruikt):d}" if gebruikt is not None else "—")
    c3.metric("Huidig saldo", f"{int(saldo):d}" if saldo is not None else "—")

    st.markdown(f"**Opvangplan:** {plan or '—'}")
    st.markdown(f"**Laatste update:** {update or '—'}")

    st.markdown("---")
    st.markdown("**Exacte rij(en) uit Excel**")
    st.dataframe(rows, use_container_width=True)

    # Download exact resultaat
    csv_bytes = rows.to_csv(index=False).encode("utf-8")
    safe_opvang = re.sub(r"[^a-z0-9_-]+", "_", str(opvang).lower())
    safe_kind   = re.sub(r"[^a-z0-9_-]+", "_", str(first[col_kind]).lower())
    st.download_button(
        "Download als CSV",
        data=csv_bytes,
        file_name=f"respijtdagen_{safe_opvang}_{safe_kind}.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption("De eerste rij in Excel wordt als **kolomnamen** gebruikt. Filtering gebeurt op **opvang** en ingevoerde **naam kind**.")
