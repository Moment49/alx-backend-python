from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from .models import Message, Notification


@receiver(post_save, sender=Message)
def notify_when_message_created(sender, instance, created, **kwargs):
    if created:
        # Create a Notification for message
        notification_user = Notification.objects.create(message=instance, recipient=instance.reciever)
        notification_user.save()
        print(f"Notification message {instance.content} recieved by user {notification_user.recipient}")
        