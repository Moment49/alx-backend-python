from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter 
from rest_framework_simplejwt import views as jwt_views


# Create a router and register our ViewSets with it.
router = routers.DefaultRouter()
# router.register(r'message', views.MessageViewSet, basename='message')
router.register(r'conversation', views.ConversationViewSet, basename='conversation')

# Nested router for messages inside conversations, this will be implemented 
# In full as I would refactor most of the flow for this.. 
conversation_router = NestedDefaultRouter(router, r'conversation', lookup='conversation')
conversation_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')

urlpatterns =[
    path('auth/register',  views.UsersCreate.as_view(), name="register"),
    path('auth/login',  views.login_view, name="login"),
    path('auth/logout',  views.logout_view, name="logout"),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
]+router.urls + conversation_router.urls