# habits/models.py
from django.db import models
from django.conf import settings

class Habit(models.Model):
    CATEGORY_CHOICES = [
        ('mood', '기분'),
        ('exercise', '운동'),
        ('happiness', '행복'),
        ('diet', '식습관'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.id} - {self.category} - {self.text}"
