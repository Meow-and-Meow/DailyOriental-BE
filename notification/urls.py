from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet


urlpatterns = [
    path('notifications/', NotificationViewSet.as_view({'get': 'list'}), name='notification-list'),
    path('notifications/<int:pk>/', NotificationViewSet.as_view({'get': 'retrieve'}), name='notification-detail'),
]
