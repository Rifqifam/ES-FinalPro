import json
import google.generativeai as genai
from threading import Lock

class ResourceManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ResourceManager, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        self.predefined_symptoms = self._load_predefined_symptoms()
        self.gemini_model = self._initialize_gemini_model()

    def _load_predefined_symptoms(self):
        try:
            with open('../data/predefined_symptoms.json', 'r') as file:
                predefined_symptoms = json.load(file)
                print("Predefined symptoms loaded successfully.")
                return predefined_symptoms
        except Exception as e:
            print(f"Error loading predefined symptoms: {e}")
            return None

    def _initialize_gemini_model(self):
        try:
            genai.configure(api_key="YOUR_API_KEY")
            gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            print("Gemini model initialized successfully.")
            return gemini_model
        except Exception as e:
            print(f"Error initializing Gemini model: {e}")
            return None

resource_manager = ResourceManager()
