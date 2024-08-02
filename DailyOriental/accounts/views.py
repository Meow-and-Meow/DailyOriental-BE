from django.shortcuts import redirect
from django.conf import settings
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model
from .serializers import CustomUserSerializer, SocialUserSerializer
from .models import CustomUser
from rest_framework.permissions import AllowAny
from django.db import transaction

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': response.data}, status=status.HTTP_201_CREATED)

class SocialUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SocialUserSerializer
    permission_classes = [permissions.AllowAny]

class CustomAuthToken(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"detail": "This endpoint only accepts POST requests."})
    
    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk })

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class KakaoLogin(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return Response({'error': 'Failed to get user info from Kakao'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = response.json()
        kakao_id = user_info['id']
        properties = user_info.get('properties', {})
        kakao_account = user_info.get('kakao_account', {})

        username = f'kakao_{kakao_id}'
        name = properties.get('nickname', '')
        gender = kakao_account.get('gender', 'male')[0]
        age_group = kakao_account.get('age_range', '20-29').split('-')[0] + 's'
        phone = kakao_account.get('phone_number', '')
        signup_reason = 'kakao_login'

        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'name': name,
                'gender': gender,
                'age_group': age_group,
                'phone': phone,
                'signup_reason': signup_reason,
            }
        )
        if not created:
            user.name = name
            user.gender = gender
            user.age_group = age_group
            user.phone = phone
            user.signup_reason = signup_reason
            user.save()

        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
        }, status=status.HTTP_200_OK)

class NaverLogin(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        url = "https://openapi.naver.com/v1/nid/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        user_info = response.json()
        return Response(user_info, status=status.HTTP_200_OK)

class KakaoCallback(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        code = request.data.get('code')
        token_url = "https://kauth.kakao.com/oauth/token"
        redirect_uri = settings.KAKAO_REDIRECT_URI
        client_id = settings.KAKAO_CLIENT_ID
        client_secret = settings.KAKAO_CLIENT_SECRET

        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
            "client_secret": client_secret,
        }

        token_response = requests.post(token_url, data=data)
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response({'error': 'Failed to obtain access token'}, status=status.HTTP_400_BAD_REQUEST)

        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        if 'id' in user_info:
            kakao_id = user_info['id']
            properties = user_info.get('properties', {})
            kakao_account = user_info.get('kakao_account', {})

            user, created = CustomUser.objects.get_or_create(
                username=kakao_id,
                defaults={
                    'name': properties.get('nickname', ''),
                    'gender': kakao_account.get('gender', 'N/A'),
                    'age_group': kakao_account.get('age_range', 'N/A'),
                }
            )

            if not created:
                user.name = properties.get('nickname', user.name)
                user.gender = kakao_account.get('gender', user.gender)
                user.age_group = kakao_account.get('age_range', user.age_group)
                user.save()

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        else:
            return Response({'error': 'Failed to obtain user info from Kakao'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
