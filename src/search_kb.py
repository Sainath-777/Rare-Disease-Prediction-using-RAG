# src/search_kb.py
import json

with open("data/diseases_final.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

kb_names = [d["name"].strip() for d in diseases]

# Search terms — one per unmatched disease
searches = [
    "tyrosinemia",
    "citrullinemia",
    "methylmalonic",
    "medium chain",
    "very long chain",
    "hyperprolinemia",
    "histidinemia",
    "glutaric",
    "methylcrotonyl",
    "methylglutaric",
    "ketothiolase",
    "carnitine deficiency",
    "carnitine palmitoy",
    "acyl-coa dehydrogenase",
    "carbamoyl",
    "acetylglutamate",
    "pompe",
    "tay",
    "niemann",
    "leigh",
    "melas",
    "merrf",
    "mitochondrial dna depletion",
    "galactosemia",
    "fructose",
    "homocystinuria",
]

for term in searches:
    hits = [n for n in kb_names if term.lower() in n.lower()]
    if hits:
        print(f"\n🔍 '{term}':")
        for h in hits:
            print(f"   {h}")
    else:
        print(f"\n❌ '{term}': NOT FOUND IN KB")