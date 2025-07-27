from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter 
from rest_framework_simplejwt import views as jwt_views

# This is for a nested NestdefaultRouter to be implemented later
# NestedDefaultRouter()

# Create a router and register our ViewSets with it.
router = routers.DefaultRouter()


router.register(r'message', views.MessageViewSet, basename='message')
router.register(r'conversation', views.ConversationViewSet, basename='conversation')


urlpatterns =[
    path('auth/register',  views.UsersCreate.as_view(), name="register"),
    path('auth/login',  views.login_view, name="login"),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]+router.urls