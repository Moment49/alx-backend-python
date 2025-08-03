from django.db import models


# Custom manager for unread messages
class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        # Override the base queryset to only return unread messages
        # Assumes you have a BooleanField named `read`
        return super().get_queryset().filter(unread=True)

    def for_user(self, user):
        # Return unread messages specifically for the given user
        # Do NOT fetch a user object again — use the one passed in
        return self.get_queryset().filter(receiver=user)