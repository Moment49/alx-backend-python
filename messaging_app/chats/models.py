from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid




class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None):
        """Creates and return a user with an email, first_name, last_name and password."""
        if not email:
            raise ValueError("User must have an email address")
        
        if not first_name:
            raise ValueError("First name must be provided")
        if not last_name:
            raise ValueError("Last name must be provided")
        
        user = self.model(email = self.normalize_email(email),
                           password=password, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, first_name=None, last_name=None):
        user = self.create_user(email, password, first_name, last_name)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using = self._db)
        return user


# Create your models here.
class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model
    to include additional fields if necessary.
    """
    ROLES = (
        ('ADMIN', 'admin'),
        ('GUEST', 'guest'),
        ('HOST', 'host')
    )
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True, verbose_name="User ID")
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    password_hash = models.CharField(blank=False)
    role = models.CharField(max_length=10, choices=ROLES, default='GUEST', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id']),
        ]
        ordering = ['date_joined'] # Order users by their creation date


    def __str__(self):
        return f"{self.email}"
    


class Message(models.Model):
    message_id  = models.URLField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    sender_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_message")
    message_body = models.TextField(null=False)
    sent_at = models.TimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['message_id'])
        ]

    def __str__(self):
        return f"{self.message_id} ({self.sender_id})"
    
class Conversation(models.Model):
    conversation_id  = models.URLField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    participants_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_conversation")
    created_at = models.TimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['message_id'])
        ]

    def __str__(self):
        return f"{self.conversation_id} ({self.participants_id})"
    