import json
import os
import time
import shutil
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

INPUT_FILE  = "data/diseases_filtered.json"
OUTPUT_FILE = "data/diseases_final.json"      # separate output — never touches source
BACKUP_FILE = "data/diseases_filtered_BACKUP.json"
CHECKPOINT  = 100

# ── Fix: keywords without trailing spaces ──
LAB_KEYWORDS = [
    "elevated", "deficiency", "accumulation", "acidosis",
    "hyperammonemia", "abnormal", "increased", "decreased",
    "enzyme", "activity", "plasma", "urine",
    "hypoglycemia", "hyperglycemia", "acidemia", "alkalosis",
    "aminoaciduria", "proteinuria", "ketonuria", "lactate",
    "ammonia", "creatine", "creatinine", "cholesterol",
    "triglyceride", "bilirubin", "transaminase", "ferritin",
    "hemoglobin", "leukocyte", "thrombocyte", "electrolyte",
    "sodium", "potassium", "calcium", "phosphorus", "magnesium",
    "glucose", "pyruvate", "carnitine", "acylcarnitine",
    "amino acid", "organic acid", "fatty acid", "mucopolysaccharide",
    "gene mutation", "chromosome", "karyotype",
    "mri", "eeg", "ecg", "echo", "biopsy", "histology",
    "imaging", "radiograph", "ultrasound", "ct scan",
    "hypocalcemia", "hypercalcemia", "hyponatremia", "hypernatremia",
    "anemia", "thrombocytopenia", "leukopenia", "pancytopenia",
    "low hemoglobin", "low platelets", "high ammonia",
    "low enzyme", "high lactate", "low glucose"
]

SKIP_TERMS = {
    "unknown", "none", "n/a", "not available",
    "uncertain", "not applicable", "no findings",
    "no specific", "varies", "variable"
}

def extract_lab_from_symptoms(symptoms):
    """Option A — keyword extraction, zero hallucination"""
    lab = []
    clean_symptoms = []
    for term in symptoms:
        term_lower = term.lower().strip()
        if any(kw in term_lower for kw in LAB_KEYWORDS):
            lab.append(term)
        else:
            clean_symptoms.append(term)
    return clean_symptoms, lab

def generate_lab_with_groq(disease_name, symptoms, retries=3):
    """Option B — Groq with retry logic on 429"""
    prompt = f"""You are a medical knowledge assistant.
List ONLY the standard laboratory findings for this rare disease.

Disease: {disease_name}
Known symptoms: {', '.join(symptoms[:6])}

Rules:
- Return ONLY real, clinically established lab findings
- Maximum 4 findings
- Short phrases only, lowercase
- No symptoms, no treatments, no explanations
- If you are not certain, return nothing at all
- Format: one finding per line, nothing else"""

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80
            )
            raw = response.choices[0].message.content.strip()
            findings = []
            for line in raw.split("\n"):
                clean = line.strip().lstrip("-•1234567890.").strip().lower()
                if (
                    clean and
                    len(clean) > 4 and
                    clean not in SKIP_TERMS and
                    not any(skip in clean for skip in SKIP_TERMS)
                ):
                    findings.append(clean)
            return findings[:4]

        except Exception as e:
            err = str(e)
            if "429" in err:
                wait = 30 * (attempt + 1)  # 30s, 60s, 90s
                print(f"  Rate limit hit — waiting {wait}s (attempt {attempt+1}/{retries})")
                time.sleep(wait)
            else:
                print(f"  Groq error: {e}")
                return []

    return []  # all retries failed — return empty, never "unknown"

# ── Step 1: Backup source file before touching anything ──
if not os.path.exists(BACKUP_FILE):
    shutil.copy(INPUT_FILE, BACKUP_FILE)
    print(f"✅ Backup created: {BACKUP_FILE}")
else:
    print(f"✅ Backup already exists: {BACKUP_FILE}")

# ── Step 2: Load source (always from original, never from output) ──
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    diseases = json.load(f)
print(f"Loaded: {len(diseases)} diseases from source\n")

# ── Step 3: Resume logic — check how many already done ──
finalized = []
start_index = 0

if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        finalized = json.load(f)
    start_index = len(finalized)
    print(f"Resuming from disease {start_index + 1} ({start_index} already done)\n")
else:
    print("Starting fresh\n")

# ── Step 4: Process ──
groq_used = 0
keyword_used = 0
empty_lab = 0

for i in range(start_index, len(diseases)):
    d = diseases[i]
    new_entry = {}

    new_entry["disease_id"]  = f"RMD{str(i+1).zfill(4)}"
    new_entry["orpha_id"]    = d.get("disease_id", "")
    new_entry["name"]        = d.get("name", "")

    raw_symptoms = d.get("key_symptoms", [])
    clean_symptoms, lab_from_keywords = extract_lab_from_symptoms(raw_symptoms)

    if lab_from_keywords:
        new_entry["key_symptoms"] = clean_symptoms
        new_entry["lab_findings"] = lab_from_keywords
        keyword_used += 1
    else:
        new_entry["key_symptoms"] = raw_symptoms
        groq_result = generate_lab_with_groq(d.get("name", ""), raw_symptoms)
        new_entry["lab_findings"] = groq_result
        if groq_result:
            groq_used += 1
        else:
            empty_lab += 1
        time.sleep(2)  # safe delay for Groq free tier

    new_entry["category"]         = d.get("category", "")
    new_entry["age_of_onset"]     = d.get("age_of_onset", "")
    new_entry["inheritance"]      = d.get("inheritance", "")
    new_entry["clinical_summary"] = d.get("clinical_summary", "")

    finalized.append(new_entry)
    print(f"[{i+1}/1500] ✓ {new_entry['disease_id']} — {new_entry['name']}")

    # Checkpoint saves to OUTPUT only — never touches source
    if (i + 1) % CHECKPOINT == 0:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(finalized, f, indent=2, ensure_ascii=False)
        print(f"\n--- Checkpoint saved at {i+1} ---\n")

# ── Step 5: Final save to output file ──
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(finalized, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done!")
print(f"Total diseases        : {len(finalized)}")
print(f"Lab from keywords     : {keyword_used}  (zero hallucination)")
print(f"Lab from Groq         : {groq_used}   (constrained prompt)")
print(f"Empty lab_findings    : {empty_lab}  (stored as [] — no noise)")
print(f"\nOutput saved to       : {OUTPUT_FILE}")
print(f"Source file untouched : {INPUT_FILE}")
print(f"\nSample entry:")
print(json.dumps(finalized[0], indent=2))