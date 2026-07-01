import json
import os
from difflib import SequenceMatcher

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "data",
        "women_diseases.json"
    )
)

with open(JSON_PATH, "r", encoding="utf-8") as file:
    DATA = json.load(file)

CONDITIONS = DATA["conditions"]

# Similarity check
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
# -----------------------------
# Match symptoms
# -----------------------------
def check_symptoms(user_input):

    user_input = user_input.lower()

    results = []

    for disease in CONDITIONS:

        matched = []

        for symptom in disease["common_symptoms"]:

            symptom_lower = symptom.lower()

            # Exact Match
            if symptom_lower in user_input:
                matched.append(symptom)

            # Similar Match
            elif similarity(symptom_lower, user_input) >= 0.72:
                matched.append(symptom)

        if matched:

            score = len(matched)

            results.append({

                "name": disease["name"],

                "description": disease.get(
                    "description",
                    "No description available."
                ),

                "category": disease.get(
                    "category",
                    "General"
                ),

                "matched": matched,

                "score": score

            })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:4]


# -----------------------------
# Gradio Function
# -----------------------------
def symptoms_checker_ui(symptoms):

    if not symptoms.strip():

        return "⚠ Please enter your symptoms."

    diseases = check_symptoms(symptoms)

    if not diseases:

        return (
            "❌ I couldn't confidently identify your symptoms.\n\n"
            "Your symptoms may not match the available database.\n\n"
            "Please consult a qualified Gynecologist or ask the Medical AI Chatbot for further guidance."
        )

    output = "Possible Conditions\n"
    output += "=" * 40 + "\n\n"

    for i, disease in enumerate(diseases, start=1):

        output += f"{i}. {disease['name']}\n"
        output += f"Category : {disease['category']}\n"
        output += f"Matched Symptoms : {', '.join(disease['matched'])}\n"
        output += f"Description : {disease['description']}\n\n"

    output += "=" * 40 + "\n"

    output += (
        "⚠ DISCLAIMER\n"
        "This symptom checker is for educational purposes only.\n"
        "The listed conditions are only possible matches and NOT a confirmed diagnosis.\n\n"
        "Please consult a qualified Gynecologist for proper examination, diagnosis, and treatment."
    )

    return output

