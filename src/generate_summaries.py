import json
import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open("data/diseases_filtered.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

to_process = [d for d in diseases if not d.get("clinical_summary")]
print(f"Diseases needing summary: {len(to_process)}")

for i, d in enumerate(diseases):
    if d.get("clinical_summary"):
        continue

    prompt = f"""Write a 1-2 sentence clinical summary for this rare disease.
Use ONLY the information provided below. Do not add anything extra.

Disease: {d['name']}
Symptoms: {', '.join(d['key_symptoms'][:6])}
Age of onset: {d['age_of_onset']}
Inheritance: {d['inheritance']}

Return only the summary. No extra text."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        d["clinical_summary"] = response.choices[0].message.content.strip()
        print(f"[{i+1}/1500] ✓ {d['name']}")

    except Exception as e:
        print(f"[{i+1}] ERROR: {e}")
        if "429" in str(e):
            print("Rate limit hit — waiting 30 seconds...")
            time.sleep(30)
        else:
            time.sleep(10)
        continue

    if (i + 1) % 50 == 0:
        with open("data/diseases_filtered.json", "w", encoding="utf-8") as f:
            json.dump(diseases, f, indent=2, ensure_ascii=False)
        print(f"--- Checkpoint saved at {i+1} ---")

    time.sleep(0.5)  # Groq is generous, 0.5s is enough

with open("data/diseases_filtered.json", "w", encoding="utf-8") as f:
    json.dump(diseases, f, indent=2, ensure_ascii=False)

print("All summaries generated!")
