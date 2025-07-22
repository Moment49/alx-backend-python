from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSets with it.
router = DefaultRouter()

router.register(r'message', views.MessageViewSet, basename='message')
router.register(r'conversation', views.ConversationViewSet, basename='conversation')

urlpatterns =[
    path('auth/register',  views.UsersCreate.as_view(), name="register"),
    path('auth/login',  views.login_view, name="login"),
]+router.urls