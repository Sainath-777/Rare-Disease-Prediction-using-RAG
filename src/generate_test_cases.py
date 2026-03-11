# src/generate_test_cases.py
import json
import random

random.seed(42)  # reproducible

with open("data/diseases_final.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

# Filter: only diseases with enough symptoms to form a meaningful query
usable = [
    d for d in diseases
    if len(d.get("key_symptoms", [])) >= 3
]

print(f"Diseases with 3+ symptoms: {len(usable)}")

# Sample 50 diseases
sampled = random.sample(usable, 100)

test_cases = []

for d in sampled:
    symptoms   = d.get("key_symptoms", [])
    labs       = d.get("lab_findings", [])
    age        = d.get("age_of_onset", "")
    inheritance = d.get("inheritance", "")

    # Build a natural-sounding query
    # Use up to 4 symptoms + up to 2 lab findings
    query_parts = symptoms[:4]
    if labs:
        query_parts += labs[:2]

    # Add age context if available and meaningful
    age_prefix = ""
    if age and age.lower() not in ["all ages", "unknown", ""]:
        age_prefix = f"{age} patient with "
    else:
        age_prefix = "Patient with "

    query = age_prefix + ", ".join(query_parts).lower()

    test_cases.append({
        "disease_id":   d["disease_id"],
        "ground_truth": d["name"],
        "query":        query
    })

# Save
with open("data/test_cases.json", "w", encoding="utf-8") as f:
    json.dump(test_cases, f, indent=2, ensure_ascii=False)

print(f"\n✅ Generated {len(test_cases)} test cases → data/test_cases.json")
print("\nSample (first 3):")
for tc in test_cases[:3]:
    print(f"\n  Disease  : {tc['ground_truth']}")
    print(f"  Query    : {tc['query']}")