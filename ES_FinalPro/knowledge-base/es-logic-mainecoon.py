import json

# Load the JSON data
with open('knowledge-disease-mainecoon.json', 'r') as file:
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


# Example symptoms input
input_symptoms = {
    "Weight_Loss": False,
    "Muscle_Loss": False,
    "Lethargy": True,
    "Appetite_Loss": False,
    "Vomit": True,
    "Cough": True,
    "Weak": True,
    "Tremor": False,
    "Open_Mouth_Breathing": True,
    "Rapid_Breathing": True,
    "Labored_Breathing": True,
    "Rapid_Heartbeat": True,
    "Weak_Pulse": True,
    "Bad_Breath": False,
    "Messy_Fur": False,
    "Frequent_Urination": False
}

# Determine the disease
result_backwardchaining = backward_chaining(input_symptoms)
# result_percentage = calculate_symptom_match_percentage(input_symptoms)

# Output the result
print("Possible diseases:", result_backwardchaining)