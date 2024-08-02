from django.urls import path
from .views import RegisterView, SocialUserCreateView, CustomAuthToken, LogoutView, KakaoLogin, NaverLogin, KakaoCallback, UserProfileView, DeleteUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('social/register/', SocialUserCreateView.as_view(), name='social-register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('kakao/login/', KakaoLogin.as_view(), name='kakao-login'),
    path('kakao/login/callback/', KakaoCallback.as_view(), name='kakao-callback'),
    path('naver/login/', NaverLogin.as_view(), name='naver-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('delete/', DeleteUserView.as_view(), name='delete-user'),
]
