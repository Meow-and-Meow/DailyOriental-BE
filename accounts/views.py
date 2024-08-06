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
