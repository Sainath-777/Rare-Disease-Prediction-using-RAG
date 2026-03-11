import sys
import os

# ✅ Add src/ to path so pipeline imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from flask import Flask, render_template, request, jsonify
from pipeline import run_pipeline

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or not data.get("symptoms", "").strip():
        return jsonify({"error": "No symptoms provided."}), 400

    patient_input = data["symptoms"].strip()

    try:
        # use_llm=True → full pipeline with Groq LLM ranking
        results = run_pipeline(patient_input, use_llm=True)

        formatted = []
        for r in results:
            formatted.append({
                "name":               r.get("name", "Unknown"),
                "confidence":         r.get("final_confidence", 0),
                "reasoning":          r.get("reasoning", "No reasoning provided."),
                "retrieval_similarity": round(r.get("retrieval_similarity", 0) * 100, 1),
                "llm_confidence":     r.get("original_llm_confidence", 0),
            })

        return jsonify({"results": formatted})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\n🧬 Rare Disease RAG System — Starting...")
    print("   Open your browser at: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)