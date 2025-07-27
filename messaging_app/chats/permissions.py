from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.validators import ValidationError

class IsParticipantOfConversationr(BasePermission):
    """
    Conversation: User can view, edit and delete messages they are a conversation of
    Message: You can only be updated or delete by Admin and You can not delete or update another persons message
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        else:
            raise ValidationError("Authentication is required to access this resource.")
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        if hasattr(obj, 'conversation'):
            if request.method == "PUT" or request.method == "PATCH":
                if obj.sender == request.user:
                    return True
                else:
                    raise ValidationError("You can not update another persons message")
            if request.method == 'DELETE':
                if obj.sender == request.user:
                    return True
                else:
                    # Check if the user is part of the conversation before deleting
                    conversation = obj.conversation
                    if request.user.role in ['ADMIN','HOST'] and request.user in conversation.participants.all():
                        print("You can delete the message because you are an admin")
                        return True
                    else:
                        raise ValidationError("You can not delete a message that is not yours")


    

            
            


