from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sender_messages")
    reciever = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reciever_messages")
    content = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message: {self.content} was sent by {self.sender} to {self.reciever}"

class Notification(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification message {self.message.content} for user {self.recipient}"