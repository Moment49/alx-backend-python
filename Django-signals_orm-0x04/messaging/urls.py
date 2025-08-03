from django.urls import path
from .views import home, dashboard_user, delete_user

urlpatterns = [
    path('', home, name="homepage"),
    path('dashboard/', dashboard_user, name="dashboard"),
    path('<uuid:user_id>/delete_account/', delete_user, name="delete_account"),
]