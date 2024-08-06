from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from missions.models import DailyInfo  # DailyInfo 모델 가져오기
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
        from missions.models import DEFAULT_HABITS  # DEFAULT_HABITS 가져오기
        return random.choice(DEFAULT_HABITS[category])

# CategoryHabitListView가 없다면 다음과 같이 정의합니다.
from rest_framework import generics
from .serializers import HabitSerializer
from .models import Habit

class CategoryHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        category = self.kwargs['category']
        return Habit.objects.filter(category=category, user=self.request.user)
