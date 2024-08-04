# missions/models.py
from django.db import models
from django.conf import settings
from datetime import datetime

class DailyInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    day_of_week = models.CharField(max_length=10, blank=True, null=True)
    week_of_month = models.IntegerField(blank=True, null=True)
    mood_completed = models.BooleanField(default=False)
    exercise_completed = models.BooleanField(default=False)
    happiness_completed = models.BooleanField(default=False)
    diet_completed = models.BooleanField(default=False)
    all_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.day_of_week = self.date.strftime('%A')
        self.week_of_month = (self.date.day - 1) // 7 + 1
        self.all_completed = all([
            self.mood_completed,
            self.exercise_completed,
            self.happiness_completed,
            self.diet_completed
        ])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.id} - {self.date}"
