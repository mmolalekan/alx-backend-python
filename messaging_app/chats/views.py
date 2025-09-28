from .models import User
from .filters import MessageFilter
from django.shortcuts import render
from .serializers import UserSerializer
from .models import Message, Conversation
from .pagination import MessagePagination
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsParticipantOfConversation]

class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    
    def perform_create(self, serializer):
        serializer.save(participants_id=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and creating messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = MessageFilter
    search_fields = ['message_body']
    pagination_class = MessagePagination
    permission_classes = [IsParticipantOfConversation]
    
    def get_queryset(self):
        # Retrieve the conversation_id from the URL and filter messages
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer, request):
        # The conversation object is available via a nested router's lookup
        try:
            conversation = Conversation.objects.get(
            id=self.kwargs.get('conversation_id')
            )
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if request.user not in conversation.participants_id.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=self.request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
