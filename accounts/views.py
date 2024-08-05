# accounts/views.py
from rest_framework import generics, permissions, status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, GuestUserSerializer, LoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

@method_decorator(csrf_exempt, name='dispatch')
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
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Submit survey result",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'survey_result': openapi.Schema(type=openapi.TYPE_STRING, description='Survey result'),
            },
            required=['survey_result']
        ),
        responses={200: openapi.Response(description='Survey result submitted')}
    )
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
