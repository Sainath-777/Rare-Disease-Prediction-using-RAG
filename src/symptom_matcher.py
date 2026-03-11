def symptom_overlap_score(query, disease):
    
    query_text = query.lower()

    symptoms = disease.get("key_symptoms", [])
    labs = disease.get("lab_findings", [])

    score = 0
    total = len(symptoms) + len(labs)

    if total == 0:
        return 0

    for s in symptoms:
        if s.lower() in query_text:
            score += 1

    for l in labs:
        if l.lower() in query_text:
            score += 1

    return score / total