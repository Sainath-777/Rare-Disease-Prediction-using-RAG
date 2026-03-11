import json

# Load knowledge base names
with open("data/diseases_final.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

kb_names = {d["name"].strip().lower(): d["name"] for d in diseases}

# Load test cases
with open("data/test_cases.json", "r", encoding="utf-8") as f:
    test_cases = json.load(f)

print(f"Total test cases : {len(test_cases)}")
print(f"Total KB diseases: {len(diseases)}\n")

matched   = []
unmatched = []

for case in test_cases:
    gt = case["ground_truth"].strip()
    if gt.lower() in kb_names:
        matched.append(gt)
    else:
        # Try to find close names for suggestion
        suggestions = [
            name for name in kb_names
            if gt.lower().split()[0] in name  # first word match
        ]
        unmatched.append({
            "ground_truth": gt,
            "suggestions": [kb_names[s] for s in suggestions[:3]]
        })

print(f"✅ Matched  : {len(matched)}")
print(f"❌ Unmatched: {len(unmatched)}\n")

if unmatched:
    print("--- Unmatched ground truths + closest KB names ---\n")
    for u in unmatched:
        print(f"  GT : {u['ground_truth']}")
        if u['suggestions']:
            for s in u['suggestions']:
                print(f"       → Suggestion: {s}")
        else:
            print(f"       → No close match found")
        print()
