# src/fix_test_cases.py
import json
from difflib import get_close_matches

with open("data/diseases_final.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

kb_names = [d["name"].strip() for d in diseases]
kb_lower  = {n.lower(): n for n in kb_names}

with open("data/test_cases.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)

print("=" * 70)
print("FUZZY MATCH REPORT — paste this back to Claude")
print("=" * 70)

for case in test_cases:
    gt = case["ground_truth"].strip()
    if gt.lower() in kb_lower:
        print(f"✅ MATCHED  : {gt}")
    else:
        matches = get_close_matches(gt, kb_names, n=3, cutoff=0.4)
        print(f"❌ NO MATCH : {gt}")
        if matches:
            for m in matches:
                print(f"   → {m}")
        else:
            print(f"   → No close match found")