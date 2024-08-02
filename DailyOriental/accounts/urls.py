# accounts/urls.py
from django.urls import path
from .views import RegisterView, CustomAuthToken, UserDetailView, SurveyResultView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('user/<str:id>/', UserDetailView.as_view(), name='user-detail'),
    path('survey/', SurveyResultView.as_view(), name='survey-result'),
]