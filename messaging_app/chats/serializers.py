from rest_framework import serializers
from .models import Message, Conversation
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only = True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['user_id','first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password= attrs.get('password')
        if len(password) and len(confirm_password) < 7:
            raise ValidationError("Password must be above 7 characters")
        else:
            if password != confirm_password:
                raise ValidationError("Password does not match")
    
    def create(self, validated_data):
        email = validated_data.pop('email')
       
        user = CustomUser.objects.create_user(email=email, **validated_data)
        # Create token for user
        Token.objects.create(user=user)

        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer() 
    class Meta:
        model = Message
        fields = ['message_id','sender', 'message_body', 'conversation']


class ConversationSerializer(serializers.ModelSerializer):
    messsages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'messages', 'participants']
        depth = 1

        