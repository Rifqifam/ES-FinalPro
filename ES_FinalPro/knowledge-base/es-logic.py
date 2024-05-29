import json

# Load the JSON data
with open('knowledge-disease-mainecoon.json', 'r') as file:
    diseases = json.load(file)

def backward_chaining(symptoms):
    possible_diseases = []
    
    for disease, info in diseases.items():
        match = True
        for symptom, value in info['symptoms'].items():
            if symptoms.get(symptom) != value:
                match = False
                break
        if match:
            possible_diseases.append(disease)
    
    return possible_diseases

def calculate_symptom_match_percentage(symptoms):
    results = {}
    
    for disease, info in diseases.items():
        total_symptoms = len(info['symptoms'])
        matched_symptoms = 0
        
        for symptom, value in info['symptoms'].items():
            if symptom in input_symptoms and input_symptoms[symptom] == value:
                matched_symptoms += 1
        
        percentage_match = (matched_symptoms / total_symptoms) * 100
        results[disease] = percentage_match
    
    return results

# Example symptoms input
input_symptoms = {
    "Weight_Loss": False,
    "Muscle_Loss": True,
    "Lethargy": True,
    "Appetite_Loss": True,
    "Vomit": False,
    "Cough": False,
    "Weak": True,
    "Tremor": True,
    "Open_Mouth_Breathing": True,
    "Rapid_Breathing": False,
    "Labored_Breathing": False,
    "Rapid_Heartbeat": False,
    "Weak_Pulse": False,
    "Bad_Breath": False,
    "Messy_Fur": False,
    "Frequent_Urination": True
}

# Determine the disease
result_backwardchaining = backward_chaining(input_symptoms)
result_percentage = calculate_symptom_match_percentage(input_symptoms)

# Output the result
print("Possible diseases:", result_backwardchaining)

for disease, percentage in result_percentage.items():
    print(f"{disease}: {percentage:.2f}% match")
