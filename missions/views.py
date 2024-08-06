# missions/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import DailyInfo
from .serializers import DailyInfoSerializer
from drf_yasg.utils import swagger_auto_schema
from habits.models import Habit
import random
from datetime import datetime

class DailyInfoView(generics.ListCreateAPIView):
    queryset = DailyInfo.objects.all()
    serializer_class = DailyInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="List or create daily info")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create daily info")
    def post(self, request, *args, **kwargs):
        user = request.user
        date_str = request.data.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Check if DailyInfo already exists for the given date
        daily_info, created = DailyInfo.objects.get_or_create(user=user, date=date)
        
        # If newly created, assign random missions
        if created:
            daily_info.mood_mission = self.get_random_habit('mood', user)
            daily_info.exercise_mission = self.get_random_habit('exercise', user)
            daily_info.happiness_mission = self.get_random_habit('happiness', user)
            daily_info.diet_mission = self.get_random_habit('diet', user)
            daily_info.save()

        serializer = self.get_serializer(daily_info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_random_habit(self, category, user):
        habits = Habit.objects.filter(category=category, user=user)
        if habits.exists():
            return random.choice(habits).text
        return None

    def get_queryset(self):
        user = self.request.user
        return DailyInfo.objects.filter(user=user)

class DailyInfoDetailView(generics.RetrieveUpdateAPIView):
    queryset = DailyInfo.objects.all()
    serializer_class = DailyInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'date'

    @swagger_auto_schema(operation_description="Retrieve or update daily info by date")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Partial update daily info by date")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return DailyInfo.objects.filter(user=user)
