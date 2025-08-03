from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import AllowAny

# Create your views here.

CustomUser = get_user_model()

def home(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
    
        if user is not None:
            login(request, user)
            # Redirect
            return redirect('dashboard')
    return render(request, 'home.html')


@login_required
def dashboard_user(request):
    return render(request, 'dashboard_user.html')


@login_required
def delete_user(request, user_id):
    # check if the user matches
    user = CustomUser.objects.get(email = request.user)
    if user_id == user.user_id:
        # Delete user account
        user.delete()
    return render(request, 'account_deleted.html')

@api_view(['GET'])
# @permission_classes([AllowAny])
def threaded_conversations(request):
    messages = Message.objects.filter(parent_message__isnull=True, sender=request.user) \
                              .select_related('sender', 'receiver') \
                              .prefetch_related('replies')

    serializer = MessageSerializer(messages, many=True)
    print(serializer)
    return Response({"data": serializer.data})



