from django.db import models
from django.conf import settings

class DailyInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    day_of_week = models.CharField(max_length=10)
    week_of_month = models.IntegerField()
    mood_completed = models.BooleanField(default=False)
    exercise_completed = models.BooleanField(default=False)
    happiness_completed = models.BooleanField(default=False)
    diet_completed = models.BooleanField(default=False)
    all_completed = models.BooleanField(default=False)
    mood_mission = models.TextField(null=True, blank=True)
    exercise_mission = models.TextField(null=True, blank=True)
    happiness_mission = models.TextField(null=True, blank=True)
    diet_mission = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.day_of_week = self.date.strftime('%A')
        first_day = self.date.replace(day=1)
        adjusted_dom = self.date.day + first_day.weekday()
        self.week_of_month = int(adjusted_dom / 7) + 1
        self.all_completed = self.mood_completed and self.exercise_completed and self.happiness_completed and self.diet_completed
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.date}"
