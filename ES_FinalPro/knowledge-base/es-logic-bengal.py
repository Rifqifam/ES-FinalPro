import json

# Load the JSON data
with open('knowledge-disease-bengal.json', 'r') as file:
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
    "Weight_Loss": True,
            "Muscle_Loss": True,
            "Lethargy": True,
            "Appetite_Loss": True,
            "Vomit": True,
            "Cough": False,
            "Weak": True,
            "Tremor": True,
            "Open_Mouth_Breathing": False,
            "Rapid_Breathing": False,
            "Labored_Breathing": False,
            "Rapid_Heartbeat": False,
            "Weak_Pulse": False,
            "Bad_Breath": True,
            "Messy_Fur": False,
            "Frequent_Urination": False,
            "Diarrhea": True,
            "Blindness": False,
            "Night_Blindness": False,
            "Increased_Thirst": False,
            "Seizures": False,
            "Blood_in_Urine": False,
            "High_Blood_Glucose_Levels": False,
            "Fatigue": False,
            "Muscle_Twitching": True
}

# Determine the disease
result_backwardchaining = backward_chaining(input_symptoms)
# result_percentage = calculate_symptom_match_percentage(input_symptoms)

# Output the result
print("Possible diseases:", result_backwardchaining)