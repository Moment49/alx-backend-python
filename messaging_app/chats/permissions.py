from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.validators import ValidationError

class IsMessageOwnerOrConversationAdmin(BasePermission):
    """
    Object-level permission to only allow owner of an object to edit it or delete messages.
    Assumes the model instance has an `sender` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
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
                print(conversation.participants.all())
                if request.user.role in ['ADMIN','HOST'] and request.user in conversation.participants.all():
                    print("You can delete the message")
                    return True
                else:
                    raise ValidationError("You can not delete a message that is not yours")
            
            


