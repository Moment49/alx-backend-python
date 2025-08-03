from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'parent_message', 'content', 'timestamp', 'replies']
    
    def get_replies(self, obj):
        replies_obj = obj.replies.all()
        return MessageSerializer(replies_obj,  many=True).data