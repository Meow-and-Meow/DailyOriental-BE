# missions/serializers.py
from rest_framework import serializers
from .models import DailyInfo

class DailyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyInfo
        fields = ['date', 'day_of_week', 'week_of_month', 'mood_completed', 'exercise_completed', 'happiness_completed', 'diet_completed', 'all_completed']
        read_only_fields = ['day_of_week', 'week_of_month', 'all_completed']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        # 기본 값을 설정하여 DailyInfo 객체 생성
        daily_info, created = DailyInfo.objects.get_or_create(
            user=user, date=validated_data['date'],
            defaults={
                'mood_completed': False,
                'exercise_completed': False,
                'happiness_completed': False,
                'diet_completed': False
            }
        )

        return daily_info
