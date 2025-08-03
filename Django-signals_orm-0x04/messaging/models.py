from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

CustomUser = get_user_model()

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receiver")
    content = models.TextField(max_length=300)
    parent_message = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="replies")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    objects = models.Manager()  # The default manager.
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Message: {self.content} was sent by {self.sender} to {self.receiver}"

class Notification(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification message {self.message.content} for user {self.recipient}"

class MessageHistory(models.Model):
    edited_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="history")
    edited_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-edited_at']

    def __str__(self):
        return f"Message History: {self.edited_message.content} between sender {self.edited_message.sender}\
        and reciever {self.edited_message.receiver} edited by {self.edited_by}"
