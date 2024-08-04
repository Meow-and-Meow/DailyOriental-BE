# missions/views.py
from rest_framework import generics, permissions
from .models import DailyInfo
from .serializers import DailyInfoSerializer
from drf_yasg.utils import swagger_auto_schema

class DailyInfoView(generics.ListCreateAPIView):
    queryset = DailyInfo.objects.all()
    serializer_class = DailyInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="List or create daily info")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create daily info")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return DailyInfo.objects.filter(user=user)

class DailyInfoDetailView(generics.RetrieveUpdateAPIView):
    queryset = DailyInfo.objects.all()
    serializer_class = DailyInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'date'

    @swagger_auto_schema(operation_description="Retrieve or update daily info by date")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Partial update daily info by date")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return DailyInfo.objects.filter(user=user)
