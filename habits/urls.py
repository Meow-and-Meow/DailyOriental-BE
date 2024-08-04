# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, CategoryHabitListView

router = DefaultRouter()
router.register(r'', HabitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/<str:category>/', CategoryHabitListView.as_view(), name='category-habit-list'),
]
