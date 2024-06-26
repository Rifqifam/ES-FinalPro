import json
import os

here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(here, 'knowledge-disease-persian.json')

# Load the JSON data
with open(filename, 'r') as file:
    diseases = json.load(file)

def backward_chaining(symptoms):
    possible_diseases = []
    
    for disease, info in diseases.items():
        match_count = 0
        total_symptoms = len(info['symptoms'])
        
        for symptom, value in info['symptoms'].items():
            if symptoms.get(symptom) == value:
                match_count += 1
        
        if match_count > 0:  # Only consider diseases with at least one matching symptom
            possible_diseases.append((disease, match_count / total_symptoms * 100))

    return sorted(possible_diseases, key=lambda x: x[1], reverse=True)

def get_highest_probability_disease_with_treatment(symptoms):
    possible_diseases = backward_chaining(symptoms)
    if not possible_diseases:
        return "No diseases match the provided symptoms."
    
    highest_probability_disease = possible_diseases[0]
    disease_name = highest_probability_disease[0]
    treatment = diseases[disease_name]["treatment"]
    return treatment

# Example symptoms input
input_symptoms = {
    "Weight_Loss": True,
    "Muscle_Loss": False,
    "Lethargy": True,
    "Appetite_Loss": True,
    "Vomit": True,
    "Cough": False,
    "Weak": True,
    "Tremor": False,
    "Open_Mouth_Breathing": False,
    "Rapid_Breathing": False,
    "Labored_Breathing": False,
    "Rapid_Heartbeat": False,
    "Weak_Pulse": True,
    "Bad_Breath": False,
    "Messy_Fur": False,
    "Frequent_Urination": True,
    "Blindness": False,
    "Night_Blindness": False,
    "Diarrhea": False,
    "Increased_Thirst": True,
    "Seizures": False,
    "Blood_in_Urine": False,
    "High_Blood_Glucose_Levels": False,
    "Fatigue": True,
    "Muscle_Twitching": False,
    "Dehydration": True,
    "Depression": True,
    "Collapse": False,
    "Fainting": False,
    "Dilated_Pupils": False,
    "Clumsiness": False,
    "Snoring": False,
    "Gagging": False,
    "Mouth_Pain": False,
    "Drooling": False,
    "Difficulty_Eating": False
}

# Determine the disease
result_backwardchaining = backward_chaining(input_symptoms)
# result_percentage = calculate_symptom_match_percentage(input_symptoms)

# Output the result
# print("Possible diseases:", result_backwardchaining)
# print(get_highest_probability_disease_with_treatment(input_symptoms))