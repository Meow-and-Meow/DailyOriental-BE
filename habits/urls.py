# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, CategoryHabitListView
habit_list = HabitViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

habit_detail = HabitViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
router = DefaultRouter()
router.register(r'', HabitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/', habit_detail, name='habit-detail'),
    path('category/<str:category>/', CategoryHabitListView.as_view(), name='category-habit-list'),
]
