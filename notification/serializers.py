from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    message_type = serializers.CharField()  # message_type을 직렬화할 필드 추가

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'url_text', 'url', 'message_type', 'created_at', 'is_read']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # message_type에 대한 명확한 레이블을 반환하도록 설정
        message_type_labels = {
            'daily_mission': 'Daily Mission',
            'health_tip': 'Health Tip',
            'acupressure_point': 'Acupressure Point'
        }
        representation['message_type'] = message_type_labels.get(instance.message_type, 'Unknown Type')
        return representation
