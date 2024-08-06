from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Habit, DEFAULT_HABITS
from .serializers import HabitSerializer
from missions.models import DailyInfo
from drf_yasg.utils import swagger_auto_schema
import random

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Create a new habit")
    def create(self, request, *args, **kwargs):
        # 클라이언트에서 user 필드를 보내지 않아도 되도록 데이터에서 제거
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.update_daily_info_missions(request.user, data['category'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(operation_description="List all habits")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, default=False)

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
        return random.choice(DEFAULT_HABITS[category])

from rest_framework import generics

class CategoryHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category = self.kwargs['category']
        return Habit.objects.filter(category=category, user=self.request.user)
