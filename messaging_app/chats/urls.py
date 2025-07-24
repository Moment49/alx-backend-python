from django.urls import path, include
from . import views
from rest_framework import routers 

# Create a router and register our ViewSets with it.
router = routers.DefaultRouter()

router.register(r'message', views.MessageViewSet, basename='message')
router.register(r'conversation', views.ConversationViewSet, basename='conversation')

urlpatterns =[
    path('auth/register',  views.UsersCreate.as_view(), name="register"),
    path('auth/login',  views.login_view, name="login"),
    path('', include(router.urls))
]