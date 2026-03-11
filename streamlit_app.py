# import streamlit as st
# from pipeline import run_pipeline

# st.title("🧬 Rare Disease Diagnostic Assistant")
# st.caption("Powered by RAG + FAISS + Groq LLM")

# symptoms = st.text_area("Enter patient symptoms:")

# if st.button("Diagnose"):
#     with st.spinner("Retrieving from knowledge base..."):
#         results = run_pipeline(symptoms)
    
#     for i, disease in enumerate(results, 1):
#         # st.subheader(f"#{i} — {disease['name']} ({disease['confidence']}%)")
#         st.subheader(f"#{i} — {disease['name']} {disease['final_confidence']}%")
#         st.write(disease['reasoning'])


import sys
import os

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from src.pipeline import run_pipeline

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RareDx — Rare Disease Diagnostic System",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #070d14;
    color: #e2eaf4;
}

.stApp {
    background-color: #070d14;
    background-image:
        linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1300px; }

/* ── Header banner ── */
.raredx-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 0 28px;
    border-bottom: 1px solid rgba(56,189,248,0.12);
    margin-bottom: 40px;
}
.raredx-logo {
    display: flex;
    align-items: center;
    gap: 14px;
}
.raredx-logo-icon {
    width: 44px; height: 44px;
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.raredx-logo-name {
    font-family: 'Syne', sans-serif;
    font-size: 24px; font-weight: 800;
    color: #ffffff; letter-spacing: -0.5px;
    display: block;
}
.raredx-logo-sub {
    font-family: 'DM Mono', monospace;
    font-size: 10px; color: #6b8aa8;
    text-transform: uppercase; letter-spacing: 1.5px;
    display: block;
}
.raredx-stats {
    display: flex; gap: 28px; align-items: center;
}
.raredx-stat { text-align: right; }
.raredx-stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 22px; font-weight: 700;
    color: #38bdf8; display: block;
}
.raredx-stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px; color: #6b8aa8;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.raredx-divider {
    width: 1px; height: 40px;
    background: rgba(56,189,248,0.12);
}

/* ── Panel labels ── */
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px; letter-spacing: 2px;
    color: #38bdf8; text-transform: uppercase;
    margin-bottom: 8px;
}
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px; font-weight: 700;
    color: #ffffff; margin-bottom: 8px;
}
.panel-desc {
    font-size: 14px; color: #6b8aa8;
    line-height: 1.7; margin-bottom: 20px;
}

/* ── Textarea override ── */
.stTextArea textarea {
    background: #101e2e !important;
    border: 1px solid rgba(56,189,248,0.15) !important;
    border-radius: 12px !important;
    color: #e2eaf4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 16px 18px !important;
    line-height: 1.7 !important;
}
.stTextArea textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important;
}
.stTextArea label {
    color: #6b8aa8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ── Button override ── */
.stButton > button {
    background: #38bdf8 !important;
    color: #070d14 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 14px 28px !important;
    width: 100% !important;
    transition: all 0.2s !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: #7dd3fc !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(56,189,248,0.3) !important;
}

/* ── Pipeline flow ── */
.pipeline-flow {
    display: flex; align-items: center;
    gap: 6px; flex-wrap: wrap;
    padding: 14px 16px;
    background: #101e2e;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px; margin-top: 16px;
}
.pf-step {
    font-family: 'DM Mono', monospace;
    font-size: 10px; color: #6b8aa8;
    white-space: nowrap;
}
.pf-step.hl { color: #38bdf8; font-weight: 500; }
.pf-arrow { color: #3d5a73; font-size: 10px; }

/* ── Disease card ── */
.disease-card {
    background: #101e2e;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    display: flex;
    overflow: hidden;
    margin-bottom: 16px;
    transition: transform 0.2s, border-color 0.2s;
}
.disease-card:hover {
    border-color: rgba(56,189,248,0.2);
    transform: translateY(-2px);
}
.card-rank {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 22px 20px;
    background: #0c1621;
    border-right: 1px solid rgba(255,255,255,0.05);
    min-width: 80px; gap: 4px;
}
.rank-num {
    font-family: 'Syne', sans-serif;
    font-size: 32px; font-weight: 800;
    line-height: 1;
}
.rank-num-1 { color: #38bdf8; }
.rank-num-2 { color: rgba(56,189,248,0.6); }
.rank-num-3 { color: rgba(56,189,248,0.3); }
.rank-tag {
    font-family: 'DM Mono', monospace;
    font-size: 8px; color: #3d5a73;
    text-transform: uppercase; letter-spacing: 0.5px;
    text-align: center; line-height: 1.4;
}
.card-content {
    flex: 1; padding: 20px 24px;
    display: flex; flex-direction: column; gap: 12px;
}
.disease-name {
    font-family: 'Syne', sans-serif;
    font-size: 17px; font-weight: 700;
    color: #ffffff; line-height: 1.3;
}
.conf-row {
    display: flex; align-items: center; gap: 12px;
}
.conf-bar-bg {
    flex: 1; height: 6px;
    background: rgba(255,255,255,0.05);
    border-radius: 99px; overflow: hidden;
}
.conf-bar-fill {
    height: 100%; border-radius: 99px;
    transition: width 0.8s ease;
}
.conf-high { background: linear-gradient(90deg, #38bdf8, #7dd3fc); }
.conf-mid  { background: linear-gradient(90deg, #fbbf24, #fde68a); }
.conf-low  { background: linear-gradient(90deg, #f87171, #fca5a5); }
.conf-label {
    font-family: 'DM Mono', monospace;
    font-size: 14px; font-weight: 500;
    min-width: 50px; text-align: right;
}
.conf-label-high { color: #38bdf8; }
.conf-label-mid  { color: #fbbf24; }
.conf-label-low  { color: #f87171; }
.reasoning {
    font-size: 13px; color: #6b8aa8;
    font-style: italic; line-height: 1.65;
    border-left: 2px solid rgba(56,189,248,0.15);
    padding-left: 12px;
}
.score-chips {
    display: flex; gap: 8px; flex-wrap: wrap;
}
.score-chip {
    background: #0c1621;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px; padding: 6px 12px;
}
.sc-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px; color: #3d5a73;
    text-transform: uppercase; letter-spacing: 0.5px;
    display: block;
}
.sc-val {
    font-family: 'DM Mono', monospace;
    font-size: 13px; color: #e2eaf4;
}

/* ── Results header ── */
.results-header {
    display: flex; align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}
.results-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px; letter-spacing: 2px;
    color: #38bdf8; text-transform: uppercase;
}
.results-meta {
    font-family: 'DM Mono', monospace;
    font-size: 11px; color: #3d5a73;
}

/* ── Disclaimer ── */
.disclaimer {
    font-family: 'DM Mono', monospace;
    font-size: 11px; color: #3d5a73;
    padding: 12px 16px;
    border: 1px solid rgba(248,113,113,0.1);
    border-radius: 8px;
    background: rgba(248,113,113,0.03);
    line-height: 1.6; margin-top: 8px;
}

/* ── Idle state ── */
.idle-box {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 80px 20px; gap: 14px; opacity: 0.4;
}
.idle-icon { font-size: 48px; }
.idle-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px; font-weight: 600; color: #6b8aa8;
}
.idle-sub { font-size: 13px; color: #3d5a73; }

/* ── Spinner text ── */
.stSpinner > div { border-top-color: #38bdf8 !important; }

/* ── Selectbox / columns ── */
div[data-testid="column"] {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="raredx-header">
  <div class="raredx-logo">
    <div class="raredx-logo-icon">🧬</div>
    <div>
      <span class="raredx-logo-name">RareDx</span>
      <span class="raredx-logo-sub">Diagnostic Intelligence System</span>
    </div>
  </div>
  <div class="raredx-stats">
    <div class="raredx-stat">
      <span class="raredx-stat-num">1,500</span>
      <span class="raredx-stat-label">Diseases</span>
    </div>
    <div class="raredx-divider"></div>
    <div class="raredx-stat">
      <span class="raredx-stat-num">93%</span>
      <span class="raredx-stat-label">Top-1 Accuracy</span>
    </div>
    <div class="raredx-divider"></div>
    <div class="raredx-stat">
      <span class="raredx-stat-num">95%</span>
      <span class="raredx-stat-label">Top-3 Accuracy</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─── Layout columns ─────────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")


# ─── Left column — Input ─────────────────────────────────────────────────────
with left:
    st.markdown('<div class="panel-label">PATIENT SYMPTOM INPUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Describe the clinical presentation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="panel-desc">
      Enter patient symptoms, lab findings, age of onset, and any relevant
      clinical observations. The system searches 1,500 indexed rare diseases
      and returns ranked differential diagnoses with confidence scores.
    </div>
    """, unsafe_allow_html=True)

    # Example selector
    examples = {
        "— Select an example —": "",
        "Urea cycle disorder (infant)":
            "Infant with poor feeding, vomiting, lethargy and hyperammonemia. Low citrulline, elevated orotic acid.",
        "Lysosomal storage (child)":
            "Child with hepatosplenomegaly, developmental regression, cherry red macula. Progressive neurological decline.",
        "Mitochondrial disease":
            "Patient with stroke-like episodes, seizures, lactic acidosis, maternal inheritance. Ragged red fibers on biopsy.",
        "Metabolic acidosis (neonate)":
            "Neonate with metabolic acidosis, ketosis, hyperammonemia, poor feeding, elevated acylcarnitines.",
    }

    choice = st.selectbox("Quick examples", list(examples.keys()), label_visibility="collapsed")

    default_text = examples[choice] if choice != "— Select an example —" else ""

    symptoms = st.text_area(
        "PATIENT SYMPTOMS / CLINICAL FINDINGS",
        value=default_text,
        height=180,
        placeholder="e.g. Infant with poor feeding, vomiting, lethargy and hyperammonemia...",
    )

    char_count = len(symptoms)
    st.markdown(
        f'<div style="font-family:\'DM Mono\',monospace;font-size:11px;color:#3d5a73;margin-top:-8px;margin-bottom:16px">'
        f'{char_count} characters · Ctrl+Enter to submit</div>',
        unsafe_allow_html=True
    )

    run = st.button("🔍  Run Diagnostic Analysis")

    # Pipeline flow diagram
    st.markdown("""
    <div class="pipeline-flow">
      <span class="pf-step">Symptom Input</span>
      <span class="pf-arrow">→</span>
      <span class="pf-step">FAISS Search</span>
      <span class="pf-arrow">→</span>
      <span class="pf-step">Symptom Scoring</span>
      <span class="pf-arrow">→</span>
      <span class="pf-step">Groq LLM Ranking</span>
      <span class="pf-arrow">→</span>
      <span class="pf-step hl">Top 3 Diagnoses</span>
    </div>
    """, unsafe_allow_html=True)


# ─── Right column — Results ──────────────────────────────────────────────────
with right:

    def confidence_class(score):
        if score >= 60: return "conf-high", "conf-label-high"
        if score >= 35: return "conf-mid",  "conf-label-mid"
        return "conf-low", "conf-label-low"

    rank_tags  = ["Primary Diagnosis", "Secondary Diagnosis", "Tertiary Diagnosis"]
    rank_class = ["rank-num-1", "rank-num-2", "rank-num-3"]

    if not run:
        # Idle state
        st.markdown("""
        <div class="idle-box">
          <div class="idle-icon">📋</div>
          <div class="idle-title">Results will appear here</div>
          <div class="idle-sub">Enter patient symptoms and run analysis</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        if not symptoms.strip():
            st.error("Please enter patient symptoms before running analysis.")
        else:
            with st.spinner("Searching 1,500 diseases — running LLM ranking..."):
                try:
                    results = run_pipeline(symptoms.strip(), use_llm=True)

                    from datetime import datetime
                    ts = datetime.now().strftime("%H:%M:%S")

                    st.markdown(f"""
                    <div class="results-header">
                      <span class="results-label">DIFFERENTIAL DIAGNOSIS</span>
                      <span class="results-meta">{len(results)} candidates · {ts}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    for i, r in enumerate(results):
                        name      = r.get("name", "Unknown")
                        conf      = r.get("final_confidence", 0)
                        reasoning = r.get("reasoning", "No reasoning provided.")
                        llm_conf  = r.get("original_llm_confidence", 0)
                        vec_sim   = round(r.get("retrieval_similarity", 0) * 100, 1)

                        bar_class, label_class = confidence_class(conf)
                        tag   = rank_tags[i]  if i < len(rank_tags)  else f"Rank {i+1}"
                        rcls  = rank_class[i] if i < len(rank_class) else "rank-num-3"

                        st.markdown(f"""
                        <div class="disease-card">
                          <div class="card-rank">
                            <span class="rank-num {rcls}">{i+1}</span>
                            <span class="rank-tag">{tag}</span>
                          </div>
                          <div class="card-content">
                            <div class="disease-name">{name}</div>
                            <div class="conf-row">
                              <div class="conf-bar-bg">
                                <div class="conf-bar-fill {bar_class}" style="width:{conf}%"></div>
                              </div>
                              <span class="conf-label {label_class}">{conf:.1f}%</span>
                            </div>
                            <div class="reasoning">{reasoning}</div>
                            <div class="score-chips">
                              <div class="score-chip">
                                <span class="sc-label">LLM Confidence</span>
                                <span class="sc-val">{llm_conf}%</span>
                              </div>
                              <div class="score-chip">
                                <span class="sc-label">Vector Similarity</span>
                                <span class="sc-val">{vec_sim}%</span>
                              </div>
                              <div class="score-chip">
                                <span class="sc-label">Hybrid Score</span>
                                <span class="sc-val">{conf:.1f}%</span>
                              </div>
                            </div>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("""
                    <div class="disclaimer">
                      ⚠ Research prototype — academic use only. Not intended for clinical diagnosis.
                      Always consult qualified medical professionals.
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Pipeline error: {str(e)}")