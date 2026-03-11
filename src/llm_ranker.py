import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# ✅ Using 70b model — better clinical reasoning quality
client = Groq(api_key=API_KEY)


def build_prompt(patient_input, candidates):
    candidate_text = ""

    for i, d in enumerate(candidates):
        lab_line = ", ".join(d["lab_findings"]) if d["lab_findings"] else "none documented"
        candidate_text += f"""
Candidate {i+1}:
Name: {d['name']}
Key Symptoms: {', '.join(d['key_symptoms'])}
Lab Findings: {lab_line}
"""

    prompt = f"""You are a clinical reasoning assistant.

Patient case:
{patient_input}

You must choose only from the candidate diseases provided below.
Rank the top 3 most likely diseases.

Rules:
- Only use the provided candidates. Do not invent diseases.
- Base reasoning strictly on symptom and lab overlap with the patient case.
- Confidence percentages must sum to exactly 100.
- Output ONLY valid JSON. No explanation outside the JSON.

Output format:
{{
  "rankings": [
    {{
      "name": "exact disease name from candidates",
      "confidence": <number>,
      "reasoning": "brief clinical reasoning based on overlapping symptoms"
    }}
  ]
}}

Candidates:
{candidate_text}
"""
    return prompt


def rank_with_groq(patient_input, candidates):
    prompt = build_prompt(patient_input, candidates)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a clinical reasoning assistant. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1024,
        response_format={"type": "json_object"}  # ✅ Forces clean JSON — no markdown fences
    )

    return response.choices[0].message.content