import re
import google.generativeai as genai
import json
from ninja import NinjaAPI, Router, File
from ninja.errors import HttpError
from ninja.files import UploadedFile
from chatroom.models import ChatNode, ChatRoom, User
from django.db import transaction
from django.shortcuts import get_object_or_404
from typing import Optional
from .models import model, predict
from .knowledge_base import parent_function as pf
from .resource_manager import resource_manager

#  UTIL FUNCTIONS

def extract_chat_room_id(title):
    match = re.search(r"Chat Room - (\d+)", title)
    if match:
        return int(match.group(1))
    else:
        return None

expert_API = NinjaAPI(
    title="Chatroom API",
    description="""
    Welcome to the Chatroom API documentation.
    
    This API allows users to:
    - Manage user accounts
    - Create and manage chat rooms
    - Send and receive messages within chat rooms
    
    So basically how this works is that
    1. User Create an account by inputting username and password
    2. Then User Login with username and password which returns user_id
    3. This user_id would be save in local storage as a way to authenticate the user chatrooms

    Use the endpoints below to interact with the API.
    """
)


# Create separate routers
chatroom_router = Router(tags=["chat-rooms"])
user_router = Router(tags=["users"])
prediction_router = Router(tags=["prediction"])


input_symptoms_bengal = {
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

input_symptoms_mainecoon = {
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


@expert_API.get("/test")
def hello(request):
    return "Hello World"
  
@chatroom_router.get("/{chat_room_id}/chat-nodes/")
def chat_nodes_in_chat_room(request, chat_room_id: int, user_id:int):
    # Retrieve all ChatNode instances for the specified ChatRoom id
    user = get_object_or_404(User, user_id=user_id)
    chat_room_title = f"Chat Room - {chat_room_id}"

    try:
        chatroom = ChatRoom.objects.get(user=user, title=chat_room_title)
    except:
        return f"Chat Room - {chat_room_id} does not exist"
    
    chat_nodes = ChatNode.objects.filter(chat_room=chatroom)

    # Serialize the queryset to JSON
    data = [{'sender': node.sender, 'date_sent': node.date_sent, 'message': node.message} for node in chat_nodes]

    return data

@chatroom_router.get("/")
def get_chat_rooms(request, user_id:int):
    user = get_object_or_404(User, user_id=user_id)
    chatrooms = ChatRoom.objects.filter(user=user)

    data = [
        {
            'id': extract_chat_room_id(room.title) ,
            'title': room.title,
            'user': {
                'user_id': room.user.user_id,
                'username': room.user.username
            },
            'date_created': room.date_created
        }
        for room in chatrooms
    ]
    return data

@chatroom_router.post("/chat-nodes/add")
@transaction.atomic  # Ensures that the operations are atomic
def add_chat_node(request, sender: str, message: str, user_id : int, chat_room_id: Optional[int] = 99):
    chat_room_title = f"Chat Room - {chat_room_id}"
    user = get_object_or_404(User, user_id=user_id)
    try:
        chat_room = ChatRoom.objects.get(user=user, title=chat_room_title)

    except ChatRoom.DoesNotExist:
        # Create a new ChatRoom if it does not exist
        chat_room = ChatRoom.objects.create(
            user=user,
            title=chat_room_title
        )

    chat_node = ChatNode.objects.create(
        sender=sender,
        message=message,
        chat_room=chat_room
    )

    return {
        'id': chat_node.id,
        'sender': chat_node.sender,
        'message': chat_node.message,
        'date_sent': chat_node.date_sent,
        'chat_room_id': chat_room.id
    }

## USER ENDPOINTS ##

@user_router.post("/signup/")
def create_user(request, username: str, user_password: str):
    user = User.objects.create(username=username, user_password=user_password)
    return {
        'user_id': user.user_id,
        'username': user.username,
    }

@user_router.post("/login/")
def login(request, username: str, user_password: str):
    try:
        user = User.objects.get(username=username)
        if user.user_password == user_password:
            return {'user_id': user.user_id}
        else:
            raise HttpError(401, "Invalid credentials")
    except User.DoesNotExist:
        raise HttpError(404, "User not found")

@user_router.get("/getall")
def list_users(request):
    users = User.objects.all()
    data = [{'user_id': user.user_id, 'username': user.username} for user in users]
    return data

@user_router.get("/{user_id}/get")
def get_user(request, user_id: int):
    try:
        user = User.objects.get(user_id=user_id)
        return {
            'user_id': user.user_id,
            'username': user.username,
            'password' : user.user_password
        }
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
    
@user_router.delete("/{user_id}/delete")
def delete_user(request, user_id: int):
    try:
        user = User.objects.get(user_id=user_id)
        user.delete()
        return {"success": True}
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
    
@prediction_router.post("/predict/")
def predict_image(request, file: UploadedFile = File(...)):
    # Class 0: Bengal
    # Class 1: Maine Coon
    # Class 2: Persian
    # Class 3: Unknown
    predicted_class, confidence_score = predict(model, file)
    return {"predicted_class": predicted_class, "confidence_score": confidence_score}

@prediction_router.post("/symptoms/")   
def get_symptoms(request, breed:str, symptoms:str):
    try:
        query = f"You have to extract only the symptoms that are in this list {list(resource_manager.predefined_symptoms[breed].keys())}. This is what the owner got to say regarding the condition of the cat: {symptoms}. The output should be the list of symtomps separated by a coma and without any extra special characters. If you don't think that there is any symptoms that matches the list, return Null"
        model_response = resource_manager.gemini_model.generate_content(query)
        reported_symptoms = [symptom.strip() for symptom in model_response.text.split(",")]
    
        symptoms_dict = {symptom: False for symptom in resource_manager.predefined_symptoms[breed].keys()}
        
        for symptom in reported_symptoms:
            if symptom in symptoms_dict:
                symptoms_dict[symptom] = True

        return {"symptoms": symptoms_dict}
    except:
        raise HttpError(500, "Internal Server Error") 
    

@prediction_router.get("/result/")
def result_cat_disease(request, cat_type:str):
    answer1, answer2 = pf.parent_function(cat_type, input_symptoms_mainecoon )    

    return {"diseases" : answer1, "treatment" : answer2}    



expert_API.add_router("/users/", user_router)
expert_API.add_router("/chat-rooms/", chatroom_router)
expert_API.add_router("/prediction/", prediction_router)