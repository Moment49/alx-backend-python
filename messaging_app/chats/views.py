from rest_framework.views import APIView, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, filters
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer, MessageSerializer, ConversationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Message, Conversation
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsMessageOwnerOrConversationAdmin


CustomUser = get_user_model()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwnerOrConversationAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sent_at', 'sender__first_name', 'sender__last_name']
    search_fields = ['sender__role', 'sender__email', 'sender__first_name', 'sender__last_name']
    
    def perform_create(self, serializer):
        # automatically pass the authenticated user as sender of the message 
        serializer.save(sender=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['created_at']
    search_fields = ['participants__email']
    
    def get_queryset(self):
        """
        This view should return a list of conversations
        for the currently authenticated user.
        """
        return Conversation.objects.filter(participants__email=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        print(pk)
        # check if the user is part of the conversation participants
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        
        # Get the copy of the request to moify the request data to be passed
        data = request.data.copy()    
        data['conversation_id'] = str(conversation.conversation_id)

        serialzer = MessageSerializer(data = data, context=self.get_serializer_context())
        if serialzer.is_valid(raise_exception=True):
            serialzer.save(sender=self.request.user)
            return Response({"message": "sent the message"})


class UsersCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            # Validate the login credentials
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # create the token to validate the user
                token, created = Token.objects.get_or_create(user=user)
                return Response({"message":"login successful", "token": token.key, "data":serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid Credentials!!! user not authenticated"},
                                status=status.HTTP_401_UNAUTHORIZED)






