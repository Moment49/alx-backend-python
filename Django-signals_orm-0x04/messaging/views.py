from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

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
    request.user.user_id 
    user = CustomUser.objects.get(email = request.user)
    if user_id == user.user_id:
        # Delete user account
        user.delete()
    return render(request, 'account_deleted.html')
