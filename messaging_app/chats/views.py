from rest_framework.views import APIView, status
from rest_framework.decorators import api_view, permission_classes, action, authentication_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, filters
from django.contrib.auth import get_user_model, logout
from .serializers import UserSerializer, LoginSerializer, MessageSerializer, ConversationSerializer, LogoutSerializer
from django.contrib.auth import authenticate
from .models import Message, Conversation
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOfConversation
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication



CustomUser = get_user_model()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sent_at', 'sender__first_name', 'sender__last_name']
    search_fields = ['sender__role', 'sender__email', 'sender__first_name', 'sender__last_name']
    
    def perform_create(self, serializer):
        # automatically pass the authenticated user as sender of the message 
        serializer.save(sender=self.request.user)
    
    def get_queryset(self):
        return  Message.objects.filter(sender__email= self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
    

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['created_at']
    search_fields = ['participants__email']
    

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
            return Response({"message": "message sent"})


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
                # check if user is active
                if not user.is_active:
                    raise AuthenticationFailed("User is not active")
                
                # Create a jwt token manually here for both refresh and access tokens
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                # Add custom data to the access token
                access_token['user_id'] = str(user.user_id) 
                access_token['username'] = user.username
               

                return Response({"token":{
                    "access_token": str(access_token),
                    "refresh_token":str(refresh),
                },"message":"login successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid Credentials!!! user not authenticated"},
                                status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication, SessionAuthentication])
def logout_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        serializer = LogoutSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            # Blacklist the token and remove then remove the user
            """
            The refresh token associated with the user
            is passed to the body of the request and blacklisted
            """
            refresh_token = serializer.validated_data['token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            # logout user if session auth used from the main django Request object
            if hasattr(request._request, 'session'):
                logout(request._request)
            return Response({"message":"Logout successfull"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"bad token"}, status=status.HTTP_400_BAD_REQUEST)







