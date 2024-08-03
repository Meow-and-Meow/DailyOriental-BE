# urls.py
from django.urls import path
from .views import RegisterView, CustomAuthToken, UserDetailView, GuestUserCreateView, SurveyResultView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('user/<str:id>/', UserDetailView.as_view(), name='user-detail'),
    path('guest/', GuestUserCreateView.as_view(), name='guest-user-create'),
    path('survey/', SurveyResultView.as_view(), name='survey-result'),
]
