import xml.etree.ElementTree as ET
import json

# ── Load product9_ages.xml → build lookup by OrphaCode ──
ages_tree = ET.parse("data/en_product9_ages.xml")
ages_root = ages_tree.getroot()

ages_lookup = {}  # { "166024": { "age_of_onset": [...], "inheritance": [...] } }

for disorder in ages_root.iter("Disorder"):
    code = disorder.findtext("OrphaCode")
    if not code:
        continue

    # Age of onset (can be multiple e.g. Infancy + Adult)
    onsets = []
    for age in disorder.iter("AverageAgeOfOnset"):
        name = age.findtext("Name")
        if name:
            onsets.append(name)

    # Inheritance
    inheritances = []
    for inh in disorder.iter("TypeOfInheritance"):
        name = inh.findtext("Name")
        if name:
            inheritances.append(name)

    ages_lookup[code] = {
        "age_of_onset": ", ".join(onsets) if onsets else "unknown",
        "inheritance": ", ".join(inheritances) if inheritances else "unknown"
    }

print(f"Ages lookup built: {len(ages_lookup)} entries")

# ── Load existing diseases_raw.json ──
with open("data/diseases_raw.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

# ── Merge ──
merged = 0
for d in diseases:
    code = d["disease_id"].replace("ORPHA", "")  # extract number
    if code in ages_lookup:
        d["age_of_onset"] = ages_lookup[code]["age_of_onset"]
        d["inheritance"]  = ages_lookup[code]["inheritance"]
        merged += 1

print(f"Merged age/inheritance for: {merged} diseases")

# ── Filter: 5+ symptoms, sort by symptom count, take top 1500 ──
filtered = [d for d in diseases if len(d["key_symptoms"]) >= 5]
filtered = sorted(filtered, key=lambda d: len(d["key_symptoms"]), reverse=True)
final = filtered[:1500]

with open("data/diseases_filtered.json", "w", encoding="utf-8") as f:
    json.dump(final, f, indent=2, ensure_ascii=False)

print(f"Final dataset saved: {len(final)} diseases")
print(f"\nSample entry:")
print(json.dumps(final[0], indent=2))