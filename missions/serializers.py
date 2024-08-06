# missions/serializers.py
from rest_framework import serializers
from .models import DailyInfo

class DailyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyInfo
        fields = [
            'date', 'day_of_week', 'week_of_month', 
            'mood_mission', 'exercise_mission', 'happiness_mission', 'diet_mission',
            'mood_completed', 'exercise_completed', 'happiness_completed', 'diet_completed', 'all_completed'
        ]
        read_only_fields = ['day_of_week', 'week_of_month', 'all_completed']
