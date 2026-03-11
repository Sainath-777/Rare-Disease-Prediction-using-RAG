import json

with open("data/diseases_raw.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

filtered = []

for d in diseases:
    symptoms = d.get("key_symptoms", [])
    
    # Only keep diseases that have at least 3 symptoms
    if len(symptoms) >= 3:
        filtered.append(d)

# Take first 800
final = filtered[:800]

with open("data/diseases_filtered.json", "w", encoding="utf-8") as f:
    json.dump(final, f, indent=2, ensure_ascii=False)

print(f"Total after filtering: {len(filtered)}")
print(f"Saved: {len(final)} diseases to diseases_filtered.json")
