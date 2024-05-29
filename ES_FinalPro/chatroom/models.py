from django.db import models
from django.utils import timezone


class ChatRoom(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
class ChatNode(models.Model):
    sender = models.CharField(max_length=100)
    date_sent = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_nodes')

    def __str__(self):
        return f"{self.sender} - {self.date_sent}"


