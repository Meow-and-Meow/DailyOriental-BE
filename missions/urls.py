# missions/urls.py
from django.urls import path
from .views import DailyInfoView, DailyInfoDetailView

urlpatterns = [
    path('', DailyInfoView.as_view(), name='dailyinfo-list-create'),
    path('<str:date>/', DailyInfoDetailView.as_view(), name='dailyinfo-detail'),
]
