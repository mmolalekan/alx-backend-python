from rest_framework import permissions
from chats.models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users and participants in a conversation to access it.
    """
    def has_permission(self, request, view):
        # Allow all authenticated users to access the view
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # A user can view a conversation if they are a participant.
        if isinstance(obj, Conversation):
            return obj.participants_id.filter(id=request.user.id).exists()
            
        # A user can view or modify a message only if they are the sender.
        if isinstance(obj, Message):
            # A user can view (GET) a message if they are a participant.
            if request.method == 'GET':
                return obj.conversation.participants_id.filter(id=request.user.id).exists()
            
            # A user can update (PUT, PATCH) or delete (DELETE) a message
            # ONLY if they are the sender.
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return obj.sender_id == request.user
        
        return False