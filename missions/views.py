# missions/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import DailyInfo, DEFAULT_HABITS
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
        return random.choice(DEFAULT_HABITS[category])

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
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        data = request.data
        if 'mood_mission' in data and instance.mood_mission:
            data.pop('mood_mission')
        if 'exercise_mission' in data and instance.exercise_mission:
            data.pop('exercise_mission')
        if 'happiness_mission' in data and instance.happiness_mission:
            data.pop('happiness_mission')
        if 'diet_mission' in data and instance.diet_mission:
            data.pop('diet_mission')
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        return DailyInfo.objects.filter(user=user)
