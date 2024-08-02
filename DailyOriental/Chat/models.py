from django.db import models
from django.contrib.auth.models import User  # Django 기본 User 모델 사용 시

class ChatMessage(models.Model):
    role = models.CharField(max_length=10)  # 'user' 또는 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"{self.role}: {self.content}"