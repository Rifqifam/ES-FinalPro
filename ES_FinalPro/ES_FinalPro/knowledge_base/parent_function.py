from .bengal import backward_chaining as bengal_backward, get_highest_probability_disease_with_treatment as treatment_bengal
from .persian import backward_chaining as persian_backward, get_highest_probability_disease_with_treatment as treatment_persian
from .mainecoon import backward_chaining as mainecoon_backward, get_highest_probability_disease_with_treatment as treatment_mainecoon

def parent_function(cat_type, symptoms):
    if cat_type == 'bengal':
        return tuple(bengal_backward(symptoms)), treatment_bengal(symptoms)
    if cat_type == 'persian':
        return tuple(persian_backward(symptoms)), treatment_persian(symptoms)
    if cat_type == 'mainecoon':
        return tuple(mainecoon_backward(symptoms)), treatment_mainecoon(symptoms)