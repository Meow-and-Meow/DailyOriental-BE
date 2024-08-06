# accounts/views.py
from rest_framework import generics, permissions, status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, GuestUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from notification.models import Notification
from django.utils import timezone
import datetime

from habits.models import Habit

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = CustomUser.objects.get(id=serializer.data['id'])
        token, created = Token.objects.get_or_create(user=user)
        self.create_default_habits(user)

        # Create initial notifications for the new user
        now = timezone.now()
        today = datetime.date.today()

        # Daily mission notification
        daily_mission_message = "오늘의 미션을 완료했는지 확인해 보세요!"
        daily_mission_url_text = "미션 확인하러 가기"
        Notification.objects.create(user=user, message=daily_mission_message, url_text=daily_mission_url_text, message_type='daily_mission')

        # Health tip notification
        health_tip_message = "AI 허준 건강 상식을 확인해 보세요!"
        health_tip_url_text = "AI 허준에게 건강 상식 물어보기"
        Notification.objects.create(user=user, message=health_tip_message, url_text=health_tip_url_text, message_type='health_tip')

        # Acupressure point notification
        acupressure_point_message = "오늘의 지압점을 확인해 보세요!"
        acupressure_point_url_text = "손 지압점 확인하러 가기"
        Notification.objects.create(user=user, message=acupressure_point_message, url_text=acupressure_point_url_text, message_type='acupressure_point')


        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def create_default_habits(self, user):
        default_habits = {
            "mood": [
                "10분 동안 명상하기",
                "감사한 일 3가지 적어보기",
                "좋아하는 노래 3곡 듣기",
                "10분 동안 하늘 쳐다보기",
                "가까운 친구와 가족에게 안부 메세지 보내기",
                "저녁식사 후 따뜻한 차 한 잔 마시기",
                "영화 한 편 보기",
                "큰 소리로 3번 웃기 '하하하'",
                "자화상 그려보기"
            ],
            "exercise": [
                "집 주변 30분 걷기",
                "스트레칭 10분 하기",
                "짧은 홈트레이닝(스쿼트, 팔굽혀펴기 등) 10분 하기",
                "계단 오르내리기",
                "점심시간 후 10분 산책하기",
                "자기 전에 간단한 스트레칭하기",
                "스쿼트 20개 하기"
            ],
            "diet": [
                "하루동안 물 8잔 마시기",
                "제철 과일 챙겨 먹기",
                "인스턴트 음식 먹지 않기",
                "정해진 시간에 식사하기",
                "식사 중 휴대폰 또는 TV 보지 않기",
                "가공식품 대신 자연식품 먹기"
            ],
            "happiness": [
                "오늘 잘한 일 3가지 생각해보기",
                "나의 강점 5가지 적기",
                "오늘 배운 새로운 것 3가지",
                "좋아하는 사진 찍기",
                "스스로에게 선물하기",
                "성취 리스트 3가지 적기",
                "기쁜 순간 3가지 적어보기",
                "나의 예쁜 점 3가지 적기"
            ]
        }
        for category, habits in default_habits.items():
            for habit in habits:
                Habit.objects.create(user=user, category=category, text=habit, default=True)

class LoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField()

class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: 'Token'}
    )
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        password = request.data.get('password')

        if not user_id or not password:
            raise AuthenticationFailed("ID와 비밀번호를 입력하세요.")
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("사용자를 찾을 수 없습니다.")

        if not user.check_password(password):
            raise AuthenticationFailed("비밀번호가 올바르지 않습니다.")
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk})

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'

class GuestUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = GuestUserSerializer
    permission_classes = [permissions.AllowAny]

class SurveyResultView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        survey_result = request.data.get('survey_result', '')

        if not survey_result:
            return Response({'error': '설문 결과가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.is_authenticated:
            return Response({'error': '인증된 사용자가 아닙니다.'}, status=status.HTTP_403_FORBIDDEN)

        user.survey_result = survey_result
        user.save()

        return Response({'survey_result': survey_result}, status=status.HTTP_200_OK)
