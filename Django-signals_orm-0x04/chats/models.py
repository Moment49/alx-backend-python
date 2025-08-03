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
        
        user = self.model(email = self.normalize_email(email), first_name=first_name, last_name=last_name)
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
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name="Email Address")
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
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
    
class Conversation(models.Model):
    conversation_id  = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    participants = models.ManyToManyField(CustomUser, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['conversation_id'])
        ]
        ordering = ['-created_at'] 

    def __str__(self):
        participant_names = ",".join([participant.first_name for participant in self.participants.all()])
        return f"conversation id: {self.conversation_id}, participants:({participant_names})"
    

class Message(models.Model):
    message_id  = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField(null=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sent_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['message_id'])
        ]
        ordering = ['sent_at'] 

    def __str__(self):
        return f"Message from {self.sender.email} in conversation:({self.conversation})"
    
