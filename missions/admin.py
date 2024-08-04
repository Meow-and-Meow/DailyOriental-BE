# missions/admin.py
from django.contrib import admin
from .models import DailyInfo

@admin.register(DailyInfo)
class DailyInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'day_of_week', 'week_of_month', 'mood_completed', 'exercise_completed', 'happiness_completed', 'diet_completed', 'all_completed')
    list_filter = ('user', 'date', 'day_of_week', 'week_of_month', 'all_completed')
