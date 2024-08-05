from django.urls import path
from .views import ChatView, AssistantMessagesView

app_name = "Chat"

urlpatterns = [
    path('chat/<str:id>/', ChatView.as_view(), name='chat'),
    path('chat/<str:id>/assistant_messages/', AssistantMessagesView.as_view(), name='assistant_messages'),
]