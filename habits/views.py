# habits/views.py
from rest_framework import viewsets, permissions, generics
from .models import Habit
from .serializers import HabitSerializer
from drf_yasg.utils import swagger_auto_schema
import random

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Create a new habit")
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.update_daily_info_missions(request.user, request.data['category'])
        return response

    @swagger_auto_schema(operation_description="List all habits")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve a habit by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a habit by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a habit by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update_daily_info_missions(self, user, category):
        daily_infos = DailyInfo.objects.filter(user=user)
        for daily_info in daily_infos:
            if category == 'mood' and daily_info.mood_mission is None:
                daily_info.mood_mission = self.get_random_habit(category, user)
            elif category == 'exercise' and daily_info.exercise_mission is None:
                daily_info.exercise_mission = self.get_random_habit(category, user)
            elif category == 'happiness' and daily_info.happiness_mission is None:
                daily_info.happiness_mission = self.get_random_habit(category, user)
            elif category == 'diet' and daily_info.diet_mission is None:
                daily_info.diet_mission = self.get_random_habit(category, user)
            daily_info.save()

    def get_random_habit(self, category, user):
        habits = Habit.objects.filter(category=category, user=user)
        if habits.exists():
            return random.choice(habits).text
        return None

class CategoryHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category = self.kwargs['category']
        user = self.request.user
        return Habit.objects.filter(user=user, category=category)

    @swagger_auto_schema(operation_description="List habits by category")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
