from bengal import backward_chaining as bengal_backward, get_highest_probability_disease_with_treatment as treatment_bengal
from persian import backward_chaining as persian_backward, get_highest_probability_disease_with_treatment as treatment_persian
from mainecoon import backward_chaining as mainecoon_backward, get_highest_probability_disease_with_treatment as treatment_mainecoon

def parent_function(cat_type, symptoms):
    if cat_type == 'bengal':
        return bengal_backward(symptoms), treatment_bengal(symptoms)
    if cat_type == 'persian':
        return persian_backward(symptoms), treatment_persian(symptoms)
    if cat_type == 'mainecoon':
        return mainecoon_backward(symptoms), treatment_mainecoon(symptoms)


# if __name__ == "__main__":
#     cat_types = ['bengal', 'persian', 'mainecoon']
#     input_symptoms = {
#     "Weight_Loss": True,
#     "Muscle_Loss": False,
#     "Lethargy": True,
#     "Appetite_Loss": True,
#     "Vomit": True,
#     "Cough": False,
#     "Weak": True,
#     "Tremor": False,
#     "Open_Mouth_Breathing": False,
#     "Rapid_Breathing": False,
#     "Labored_Breathing": False,
#     "Rapid_Heartbeat": False,
#     "Weak_Pulse": True,
#     "Bad_Breath": False,
#     "Messy_Fur": False,
#     "Frequent_Urination": True,
#     "Blindness": False,
#     "Night_Blindness": False,
#     "Diarrhea": False,
#     "Increased_Thirst": True,
#     "Seizures": False,
#     "Blood_in_Urine": False,
#     "High_Blood_Glucose_Levels": False,
#     "Fatigue": True,
#     "Muscle_Twitching": False,
#     "Dehydration": True,
#     "Depression": True,
#     "Collapse": False,
#     "Fainting": False,
#     "Dilated_Pupils": False,
#     "Clumsiness": False,
#     "Snoring": False,
#     "Gagging": False,
#     "Mouth_Pain": False,
#     "Drooling": False,
#     "Difficulty_Eating": False
# }
#     for cat_type in cat_types:
#         print(f"Results for {cat_type}: {parent_function(cat_type, input_symptoms)}")
