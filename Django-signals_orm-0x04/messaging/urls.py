from django.urls import path
from .views import home, dashboard_user, delete_user, threaded_conversations, inbox_view

urlpatterns = [
    path('', home, name="homepage"),
    path('dashboard/', dashboard_user, name="dashboard"),
    path('<uuid:user_id>/delete_account/', delete_user, name="delete_account"),
    path('api/threaded_conversations/', threaded_conversations, name="threaded_messages"),
    path('inbox_view/unread/', inbox_view, name="inboxunread")
]