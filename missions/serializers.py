# missions/serializers.py
from rest_framework import serializers
from .models import DailyInfo

class DailyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyInfo
        fields = '__all__'
