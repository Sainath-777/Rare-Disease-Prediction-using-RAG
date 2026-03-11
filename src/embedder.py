import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# ✅ Correct file name
DATA_PATH = "data/diseases_final.json"
INDEX_PATH = "embeddings/faiss_index.bin"
META_PATH  = "embeddings/metadata.json"

os.makedirs("embeddings", exist_ok=True)


def load_diseases():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def disease_to_text(disease):
    """
    Converts a disease entry into embedding-friendly text.
    - category   → skipped (empty for all 1500 diseases)
    - lab_findings → included only when non-empty (7 diseases have none)
    """
    name        = disease.get("name", "Unknown")
    symptoms    = ", ".join(disease.get("key_symptoms", []))   or "not specified"
    age         = disease.get("age_of_onset", "unknown")
    inheritance = disease.get("inheritance", "unknown")
    summary     = disease.get("clinical_summary", "")

    # ✅ Only add lab findings line if data actually exists
    lab_list = disease.get("lab_findings", [])
    lab_line = f"    Lab Findings: {', '.join(lab_list)}\n" if lab_list else ""

    return (
        f"    Disease: {name}\n"
        f"    Key Symptoms: {symptoms}\n"
        f"{lab_line}"
        f"    Age of Onset: {age}\n"
        f"    Inheritance: {inheritance}\n"
        f"    Summary: {summary}\n"
    )


def main():
    print("Loading diseases_final.json ...")
    diseases = load_diseases()
    print(f"✅ Total diseases loaded: {len(diseases)}")

    # Quick sanity check — catch empty lab_findings count
    empty_labs = sum(1 for d in diseases if not d.get("lab_findings"))
    print(f"   Diseases with empty lab_findings: {empty_labs}  (will be skipped in embedding text)")

    print("\nLoading embedding model: all-MiniLM-L6-v2 ...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("\nGenerating embeddings ...")
    texts = [disease_to_text(d) for d in diseases]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)
    embeddings = np.array(embeddings).astype("float32")

    print(f"\nEmbedding shape: {embeddings.shape}")  # Expected: (1500, 384)

    print("Building FAISS index ...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"✅ Vectors in FAISS index: {index.ntotal}")

    print("\nSaving FAISS index  →", INDEX_PATH)
    faiss.write_index(index, INDEX_PATH)

    print("Saving metadata     →", META_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(diseases, f, indent=2, ensure_ascii=False)

    print("\n✅ Phase 2 complete. Embeddings rebuilt for 1500 diseases.")


if __name__ == "__main__":
    main()