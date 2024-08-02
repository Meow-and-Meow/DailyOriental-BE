# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, GuestUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from collections import Counter

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

class CustomAuthToken(ObtainAuthToken):
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
        survey_data = request.data.get('survey_data', [])

        if len(survey_data) != 30:
            return Response({'error': '설문 데이터가 올바르지 않습니다. 30개의 문항이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        counter = Counter(survey_data)
        max_count = max(counter.values())
        results = [k for k, v in counter.items() if v == max_count]

        result_mapping = {1: '태양인', 2: '태음인', 3: '소양인', 4: '소음인'}
        survey_result = ','.join([result_mapping.get(result, '') for result in results])

        return Response({'survey_result': survey_result}, status=status.HTTP_200_OK)
