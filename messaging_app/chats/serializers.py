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
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['user_id','first_name', 'last_name', 'email', 'password', 'confirm_password', 'full_name']

    def get_full_name(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}"
        return full_name

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password= attrs.get('password')
        if len(password) and len(confirm_password) < 7:
            raise ValidationError("Password must be above 7 characters")
        else:
            if password != confirm_password:
                raise ValidationError("Password does not match")
            
        return attrs
    
    def create(self, validated_data):
        email = validated_data.pop('email')

        # Pop the validated_confirmpassword before saving the user
        confirm_password = validated_data.pop('confirm_password')
       
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

        