import json
from pipeline import run_pipeline

TOP1  = 0
TOP3  = 0
TOTAL = 0
ERRORS = 0

with open("data/test_cases.json", encoding="utf-8") as f:
    test_cases = json.load(f)

print(f"Running evaluation on {len(test_cases)} test cases...\n")

for i, case in enumerate(test_cases):

    patient_input = case["query"]
    truth         = case["ground_truth"]

    try:
        result      = run_pipeline(patient_input, use_llm=False)
        predictions = [r["name"] for r in result]

        TOTAL += 1

        top1_correct = predictions[0] == truth
        top3_correct = truth in predictions[:3]

        if top1_correct:
            TOP1 += 1
        if top3_correct:
            TOP3 += 1

        # ✅ Print each result so you can see what's happening
        status = "✅" if top1_correct else ("🔶" if top3_correct else "❌")
        print(f"[{i+1:03d}] {status}  GT: {truth}")
        if not top1_correct:
            print(f"          P1: {predictions[0]}")
            if top3_correct:
                print(f"          Found in Top-3")

    except Exception as e:
        ERRORS += 1
        print(f"[{i+1:03d}] ⚠️  ERROR on: {truth}")
        print(f"          {e}")

print("\n" + "=" * 50)
print("EVALUATION RESULTS")
print("=" * 50)
print(f"Total cases   : {TOTAL}")
print(f"Errors skipped: {ERRORS}")
print(f"Top-1 Accuracy: {TOP1}/{TOTAL} = {round(TOP1/TOTAL*100, 1)}%")
print(f"Top-3 Accuracy: {TOP3}/{TOTAL} = {round(TOP3/TOTAL*100, 1)}%")
print("=" * 50)