# accounts/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)  # 요청 데이터를 출력하여 디버깅
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(id=response.data['id'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': response.data})

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
