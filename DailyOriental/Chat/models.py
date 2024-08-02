from django.conf import settings
from django.db import models

class ChatMessage(models.Model):
    role = models.CharField(max_length=10)  # 'user' 또는 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"{self.role}: {self.content}"
