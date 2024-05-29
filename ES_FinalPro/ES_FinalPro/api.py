from ninja import NinjaAPI
from ninja.errors import HttpError
from chatroom.models import ChatNode, ChatRoom


expert_API = NinjaAPI()

@expert_API.get("/hello")
def hello(request):
    return "Hello world"

@expert_API.get("/chat-room/{chat_room_id}/chat-nodes/")
def chat_nodes_in_chat_room(request, chat_room_id: int):
    # Retrieve all ChatNode instances for the specified ChatRoom id
    chat_nodes = ChatNode.objects.filter(chat_room_id=chat_room_id)

    # Serialize the queryset to JSON
    data = [{'sender': node.sender, 'date_sent': node.date_sent, 'message': node.message} for node in chat_nodes]

    return data

@expert_API.get("/chat-rooms/")
def get_chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()

    data = [{'id': room.id, 'title': room.title, 'date_created': room.date_created} for room in chat_rooms]

    return data

@expert_API.post("/chat-room/{chat_room_id}/chat-nodes/")
def add_chat_node(request, chat_room_id: int, sender: str, message: str):
    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
    except ChatRoom.DoesNotExist:
        # Create a new ChatRoom if it does not exist
        chat_room = ChatRoom.objects.create(
            title=f"New Chat Room {chat_room_id}"
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
        'chat_room_id': chat_room_id
    }