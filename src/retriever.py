import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

# INDEX_PATH = "embeddings/faiss_index.bin"
# META_PATH  = "embeddings/metadata.json"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE, "embeddings", "faiss_index.bin")
META_PATH  = os.path.join(BASE, "embeddings", "metadata.json")

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

print("Loading metadata...")
with open(META_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)


def embed_query(query):
    return model.encode([query]).astype("float32")


def retrieve(query, top_k=5):

    print("Embedding query...")
    query_vector = embed_query(query)

    print("Searching FAISS index...")
    distances, indices = index.search(query_vector, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        disease   = metadata[idx]
        distance  = float(distances[0][i])
        similarity = 1 / (1 + distance)

        results.append({
            "rank":                i + 1,
            "disease_id":          disease["disease_id"],
            "name":                disease["name"],
            "retrieval_similarity": similarity,
            "key_symptoms":        disease.get("key_symptoms", []),  # ✅ safe
            "lab_findings":        disease.get("lab_findings", [])   # ✅ safe — handles 7 empty
        })

    return results