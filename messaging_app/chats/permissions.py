from rest_framework.validators import ValidationError
from rest_framework import permissions, exceptions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Conversation: User can view, edit and delete messages they are a conversation of
    Message: You can only be updated or delete by Admin and You can not delete or update another persons message
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated and not request.user:
            raise ValidationError("Authentication is required to access this resource.")
        return True            
            
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Message : This will get the conversation attribute of the message obj
        if hasattr(obj, 'conversation'):
            # Get the conversation object
            conversation = obj.conversation
            if request.method == "PUT" or request.method == "PATCH":
                if obj.sender == request.user:
                    return True
                else:
                    raise ValidationError("You can not update another persons message")
           
            if request.method == 'DELETE':
                if obj.sender == request.user:
                    return True
                else:
                    # Check if the user is part of the conversation and user role is ADMIN or HOST before deleting
                    if request.user.role in ['ADMIN','HOST'] and request.user in conversation.participants.all():
                        print("You can delete the message because you are an admin")
                        return True
                    else:
                        raise ValidationError("You can not delete a message that is not yours")
        
        # This will handle the Conversations
        if hasattr(obj, 'participants'):
            participants = obj.participants
            print(f"Test perm: {participants.all()}")
            if request.user.role in ['ADMIN', 'HOST'] and request.user in obj.participants.all():
                return True
            else:
                raise exceptions.PermissionDenied("You must be a participant and Admin to delete a conversation")
        return False
          



    

            
            


