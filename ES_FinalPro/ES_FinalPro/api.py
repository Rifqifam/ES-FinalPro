import re
from ninja import NinjaAPI, Router
from ninja.errors import HttpError
from ninja.files import UploadedFile
from chatroom.models import ChatNode, ChatRoom, User
from django.db import transaction
from django.shortcuts import get_object_or_404


#  UTIL FUNCTIONS

def extract_chat_room_id(title):
    match = re.search(r"Chat Room - (\d+)", title)
    if match:
        return int(match.group(1))
    else:
        return None

expert_API = NinjaAPI()

# Create separate routers
chatroom_router = Router(tags=["chat-rooms"])
user_router = Router(tags=["users"])

@expert_API.get("/hello")
def hello(request):
    return "Hello world"

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

@chatroom_router.post("/{chat_room_id}/chat-nodes/add")
@transaction.atomic  # Ensures that the operations are atomic
def add_chat_node(request, chat_room_id: int, sender: str, message: str, user_id : int):
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
    

expert_API.add_router("/chat-rooms/", chatroom_router)
expert_API.add_router("/users/", user_router)