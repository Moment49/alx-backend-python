from rest_framework import serializers
from .models import Message, Conversation
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['user_id','first_name', 'last_name', 'email', 'password', 'confirm_password', 'full_name']
        read_only_fields = ['user_id', 'full_name', 'role']

    def get_full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}"
        return full_name

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password= attrs.get('confirm_password')

        if len(password) and len(confirm_password) < 7:
            raise serializers.ValidationError("Password must be above 7 characters")
        else:
            if password != confirm_password:
                raise serializers.ValidationError("Password does not match")
            
        return attrs
    
    def create(self, validated_data):
        email = validated_data.pop('email')

        # Pop the validated_confirmpassword before saving the user
        confirm_password = validated_data.pop('confirm_password')
       
        user = CustomUser.objects.create_user(email=email, **validated_data)


        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
  

class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(read_only=True)
    sender = UserSerializer(read_only=True)
    conversation_ref = serializers.SerializerMethodField() 
    # conversation_id = serializers.UUIDField(write_only=True)
   
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'conversation_ref']
        read_only_fields = ['message_id', 'conversation_ref']
    
    def get_conversation_ref(self, obj):
        """Get the conversation id"""
        return obj.conversation.conversation_id
    
    def validate(self, attrs):
        """
        Validates the message before it's sent:
        - Ensures the message body is not empty.
        - Confirms the user is part of the conversation.
        - Prevents sending messages to conversations without participants.
        """
        req_user = self.context.get("user")
        message_body = attrs.get("message_body")
        
        # Get conversation_id from the view's kwargs
        conversation_id = self.context["view"].kwargs.get("conversation_pk")

        # Check for empty message body
        if not message_body and message_body.strip() == "":
            raise serializers.ValidationError("Message body cannot be empty.")

        # Validate conversation existence
        try:
            converse = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation does not exist.")

        all_participants = converse.participants.all()
       
        # Check if conversation has participants
        if not all_participants.exists():
            raise serializers.ValidationError("Cannot send message to a conversation without participants.")
       
        # Check if the user is a participant 
        if not all_participants.filter(user_id=req_user.user_id).exists():
            raise serializers.ValidationError("You are not a participant of this converse, hence you cant send a message")

        return attrs
    
    def create(self, validated_data):
        # Pop the validated data 
        message_body = validated_data.pop("message_body")
        
        # Create the message with the validated_data and return the message object added
        message = Message.objects.create(message_body=message_body, **validated_data)
        message.save()
        return message
    
    def update(self, instance, validated_data):
        # update the message body
        instance.message_body = validated_data.get("message_body", instance.message_body)
        instance.save()

        return instance



class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'messages', 'participants']
        read_only_fields = ["conversation_id", "messages", "created_at"]
    
    def validate_participants(self, value):
        """Validate at least one participants before you create a conversation"""
        if not value:
             raise serializers.ValidationError(
            "You must add at least one participant to create a conversation."
        )
        return value
    
    def create(self, validated_data):
        """This method is to create a conversation"""
        participants = validated_data.pop('participants')
        # Get the user from context
        user = self.context.get('user')

        # Create the conversation and add the participants along with user
        conversations = Conversation.objects.create()
        conversations.participants.add(*participants)

        # Automatically add the user as a participant after the validation check
        conversations.participants.add(user)

        conversations.save()

        return conversations

    def update(self, instance, validated_data):
        """This method is to update the conversation"""
        participants_data = validated_data.pop("participants")
     
        # Get the authenticated user and add as well so user will not be removed
        user = self.context.get("user")

        if participants_data is not None:
            # Replace the existing conversation participants by adding more participates or removing more participants
            # I will refactor this to use a separate action for add or remove participants in the viewset
            instance.participants.set(participants_data)

            # Add the user
            instance.participants.add(user)
        
            instance.save()
        
        return instance



        