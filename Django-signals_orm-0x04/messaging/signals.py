from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


# Signal triggered after a Message is saved to the database
@receiver(post_save, sender=Message)
def notify_when_message_created(sender, instance, created, **kwargs):
    if created:
        # If the message was just created (not updated), create a notification for the receiver
        notification_user = Notification.objects.create(message=instance, recipient=instance.receiver)
        notification_user.save()
        print(f"Notification message {instance.content} recieved by user {notification_user.recipient}")

# Signal triggered just before a Message is saved (either created or updated)
@receiver(pre_save, sender=Message)
def log_edited_messages(sender, instance, **kwargs):
     # Purpose: Detect if an existing message is being edited and log the previous version to MessageHistory
    # Check if the message already exists in the database (i.e., it's not a new message)

    if instance.pk:
        # Fetch the current version of the message from the database
        old_message = Message.objects.get(pk = instance.pk)
        # Compare the new content (about to be saved) with the old one
        if instance.content != old_message.content:
            # Check if the curret message and olde message match if not save old message to history

            # Save the original message details to MessageHistory for record-keeping
            message_history = MessageHistory.objects.create(edited_by=instance.sender, old_content=old_message.content, 
                                                            edited_message=old_message)
            message_history.save()

            # Mark the message as edited (useful for UI display like showing 'edited')
            instance.is_edited = True
            print(f"This message {old_message.content} has been edited ")
            

@receiver(post_delete, sender=CustomUser)
def delete_user_notify(sender, instance, **kwargs):
    # Delete all messages, notification and history
    if instance:
        Message.objects.filter(sender=instance).delete()
        Notification.objects.filter(recipient=instance).delete()
        MessageHistory.objects.filter(edited_by=instance).delete()
        print(f"All the messages, notifications and message history for user {instance.first_name} has been deleted")
        
