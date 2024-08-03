from django.urls import path
from .views import ChatView

app_name = "Chat"

urlpatterns = [
    path('chat/<int:user_id>/', ChatView.as_view(), name='chat'),
]
