import uuid
from django.utils import timezone
from django.db import models

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, default='admin')
    user_password = models.CharField(max_length=10, default=123)

    def __str__(self):
        return self.username
    
class ChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms')
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return self.title
    
class ChatNode(models.Model):
    sender = models.CharField(max_length=100)
    date_sent = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_nodes')

    def __str__(self):
        return f"{self.sender} - {self.date_sent}"
    

