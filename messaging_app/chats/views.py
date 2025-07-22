from rest_framework.views import APIView, status
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer, MessageSerializer, ConversationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Message, Conversation

CustomUser = get_user_model()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer



class UsersCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
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






