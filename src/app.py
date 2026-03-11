import streamlit as st
from pipeline import run_pipeline

st.title("🧬 Rare Disease Diagnostic Assistant")
st.caption("Powered by RAG + FAISS + Groq LLM")

symptoms = st.text_area("Enter patient symptoms:")

if st.button("Diagnose"):
    with st.spinner("Retrieving from knowledge base..."):
        results = run_pipeline(symptoms)
    
    for i, disease in enumerate(results, 1):
        # st.subheader(f"#{i} — {disease['name']} ({disease['confidence']}%)")
        st.subheader(f"#{i} — {disease['name']} {disease['final_confidence']}%")
        st.write(disease['reasoning'])