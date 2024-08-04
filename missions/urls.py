# missions/urls.py
from django.urls import path
from .views import DailyInfoView, DailyInfoDetailView

urlpatterns = [
    path('', DailyInfoView.as_view(), name='daily-info-list-create'),
    path('<date>/', DailyInfoDetailView.as_view(), name='daily-info-detail'),
]
