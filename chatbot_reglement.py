# ------------------------------------------------------------
# 🤖 Chatbot – Huishoudelijk Reglement & Opvangcontract
# Verbeterd: meertalige embeddings + HYBRIDE retrieval (BM25 + vector)
# en striktere, zinsgebaseerde antwoorden met bron-snippets.
# ------------------------------------------------------------

import re
from pathlib import Path
from typing import List, Tuple

import streamlit as st

# LangChain / loaders / vector store
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Klassieke keyword retriever
from rank_bm25 import BM25Okapi

st.set_page_config(page_title="Kinderopvang Reglement Chatbot", page_icon="🤖", layout="wide")

DATA_FILES = [
    "Bijlage 1 Huishoudelijk reglement 20251001.docx",
    "Opvangcontract kinderopvang 20251001 (1).docx",
]

# ✅ Meertalig embed-model – beter voor NL:
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# -----------------------
# Tekst utils
# -----------------------
def clean_text(t: str) -> str:
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

def sent_tokenize(text: str) -> List[str]:
    # simpele NL/EN zinsdeling
    sents = re.split(r"(?<=[\.\?\!])\s+", text.strip())
    return [s for s in sents if s]

@st.cache_data(show_spinner=False)
def load_documents(files: List[str]):
    docs = []
    for f in files:
        p = Path(f)
        if not p.exists():
            st.warning(f"⚠ Bestand niet gevonden: {p}")
            continue
        loader = Docx2txtLoader(str(p))
        loaded = loader.load()
        for d in loaded:
            d.metadata = d.metadata or {}
            d.metadata["source_file"] = p.name
        docs.extend(loaded)
    return docs

@st.cache_resource(show_spinner=False)
def build_indexes(_docs, chunk_size: int = 900, chunk_overlap: int = 150):
    """
    Cache-fix: _docs met underscore.
    Bouwt:
      1) FAISS vector-index (semantisch)
      2) BM25 index (keyword)
    """
    docs = _docs

    # iets fijnmaziger splitsen helpt gericht zoeken
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[ "\n\n", "\n", "• ", "- ", ". ", "? ", "! ", "; "],
    )
    chunks = splitter.split_documents(docs)
    for d in chunks:
        d.page_content = clean_text(d.page_content)

    # 1) Vector store
    emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vstore = FAISS.from_documents(chunks, emb)

    # 2) BM25 corpus
    corpus_texts = [c.page_content for c in chunks]
    tokenized = [re.findall(r"[A-Za-zÀ-ž0-9\-]+", t.lower()) for t in corpus_texts]
    bm25 = BM25Okapi(tokenized)

    # we bewaren ook de mapping naar metadata
    meta = [c.metadata for c in chunks]

    return {
        "vstore": vstore,
        "bm25": bm25,
        "corpus": corpus_texts,
        "meta": meta,
    }

def make_citation(metadata: dict) -> str:
    return metadata.get("source_file", "bron")

def hybrid_retrieve(indexes, query: str, k_vec=4, k_kw=6) -> List[Tuple[str, dict]]:
    """Combineer vectorhits + BM25 keywordhits en dedup."""
    vstore = indexes["vstore"]
    bm25 = indexes["bm25"]
    corpus = indexes["corpus"]
    meta = indexes["meta"]

    # Vector hits
    vec_docs = vstore.similarity_search(query, k=k_vec)
    vec_pairs = [(d.page_content, d.metadata) for d in vec_docs]

    # BM25 hits (keyword)
    q_tokens = re.findall(r"[A-Za-zÀ-ž0-9\-]+", query.lower())
    scores = bm25.get_scores(q_tokens)
    kw_idx = list(sorted(range(len(corpus)), key=lambda i: scores[i], reverse=True))[:k_kw]
    kw_pairs = [(corpus[i], meta[i]) for i in kw_idx if scores[i] > 0]

    # Merge + dedup op tekst
    seen = set()
    merged: List[Tuple[str, dict]] = []
    for pair in vec_pairs + kw_pairs:
        key = pair[0][:80]  # hash op prefix
        if key not in seen:
            seen.add(key)
            merged.append(pair)
    return merged

def build_answer(query: str, ctx: List[Tuple[str, dict]], must_contain_query_terms=True) -> str:
    """
    Bouw een helder antwoord:
    - kies zinnen die de query-termen bevatten (respijt, ziekte, IKT, …)
    - val terug op compact contextfragment als er geen exacte match is
    """
    if not ctx:
        return "Ik vond geen relevante passage in het reglement/contract voor deze vraag."

    q_terms = set(re.findall(r"[A-Za-zÀ-ž0-9\-]{3,}", query.lower()))
    picked = []
    for text, meta in ctx:
        for sent in sent_tokenize(text):
            s_norm = sent.lower()
            if not q_terms or any(t in s_norm for t in q_terms):
                picked.append((sent.strip(), meta))
        if len(picked) >= 8:
            break

    parts = []
    parts.append("**Antwoord (gebaseerd op reglement/contract):**")
    if picked:
        bullets = []
        for s, _m in picked[:6]:
            bullets.append("• " + s)
        parts.append("\n".join(bullets))
    else:
        # val terug op het allereerste fragment
        parts.append(ctx[0][0][:400])

    parts.append("\n**Relevante bronfragmenten:**")
    for text, meta in ctx[:3]:
        cite = make_citation(meta)
        snippet = " ".join(text.split())
        if len(snippet) > 300:
            snippet = snippet[:300] + "…"
        parts.append(f"- _Bron: {cite}_ — “{snippet}”")

    parts.append("\n> Antwoorden zijn strikt gebaseerd op de aangeleverde documenten.")
    return "\n".join(parts)

# -----------------------
# UI
# -----------------------
st.title("🤖 Chatbot – Huishoudelijk Reglement & Opvangcontract")
st.caption("De bot antwoordt uitsluitend op basis van de twee documenten en toont bronfragmenten.")

with st.sidebar:
    st.subheader("📄 Ingeladen documenten")
    for f in DATA_FILES:
        st.write(f"• {f}")
    st.markdown("---")
    k_vec = st.slider("Vector-fragmenten (k)", 2, 10, 4)
    k_kw = st.slider("Keyword-fragmenten (k)", 2, 10, 6)
    st.caption("Tip: verhoog k_kw voor beleids/term-vragen (bv. respijt, IKT).")

docs = load_documents(DATA_FILES)
if not docs:
    st.error("Geen documenten gevonden. Zorg dat de DOCX-bestanden in dezelfde map staan als dit script.")
    st.stop()

indexes = build_indexes(docs)

if "history" not in st.session_state:
    st.session_state["history"] = []

q = st.text_input("💬 Je vraag (bv. 'Wat zegt het Opvangcontract over respijt?')")
if q:
    # eenvoudige router: als 'contract' in vraag → licht prefereren naar contract-hits
    ctx = hybrid_retrieve(indexes, q, k_vec=k_vec, k_kw=k_kw)
    ans = build_answer(q, ctx)
    st.session_state["history"].append({"q": q, "a": ans})

for turn in reversed(st.session_state["history"]):
    with st.chat_message("user"):
        st.write(turn["q"])
    with st.chat_message("assistant"):
        st.markdown(turn["a"])
