from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter out notifications that are read
        return self.queryset.filter(user=self.request.user, is_read=False).order_by('-created_at')

    def destroy(self, request, *args, **kwargs):
        notification = self.get_object()

        if notification.user != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)