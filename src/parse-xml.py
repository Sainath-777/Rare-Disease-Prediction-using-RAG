import xml.etree.ElementTree as ET
import json

# Load the XML file
tree = ET.parse("data/en_product4.xml")
root = tree.getroot()

diseases = []

for disorder_set in root.iter("HPODisorderSetStatus"):
    disorder = disorder_set.find("Disorder")
    if disorder is None:
        continue

    orpha_code = disorder.findtext("OrphaCode")
    name = disorder.find("Name").text

    # Collect symptoms with frequency
    symptoms_all = []
    frequent_symptoms = []

    assoc_list = disorder.find("HPODisorderAssociationList")
    if assoc_list:
        for assoc in assoc_list.findall("HPODisorderAssociation"):
            hpo_term = assoc.find(".//HPOTerm")
            frequency = assoc.find(".//HPOFrequency/Name")

            if hpo_term is not None:
                term = hpo_term.text
                freq = frequency.text if frequency is not None else ""

                symptoms_all.append(term)

                # Prioritize very frequent and frequent symptoms
                if "Very frequent" in freq or "Frequent" in freq:
                    frequent_symptoms.append(term)

    # Use frequent ones first, then fill up to 10
    key_symptoms = frequent_symptoms[:10] if frequent_symptoms else symptoms_all[:10]

    diseases.append({
        "disease_id": f"ORPHA{orpha_code}",
        "name": name,
        "key_symptoms": key_symptoms,
        "category": "",        # fill later
        "age_of_onset": "",    # fill later
        "inheritance": "",     # fill later
        "clinical_summary": "" # generate later with Claude
    })

# Save output
with open("data/diseases_raw.json", "w", encoding="utf-8") as f:
    json.dump(diseases, f, indent=2, ensure_ascii=False)

print(f"Done! Total diseases parsed: {len(diseases)}")


