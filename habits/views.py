# habits/views.py
from rest_framework import viewsets, permissions, generics
from .models import Habit
from .serializers import HabitSerializer
from drf_yasg.utils import swagger_auto_schema

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Create a new habit")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

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
