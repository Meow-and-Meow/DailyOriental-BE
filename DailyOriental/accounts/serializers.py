# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'name', 'gender', 'age', 'phone', 'reason', 'survey_result')
        extra_kwargs = {
            'password': {'write_only': True},
            'survey_result': {'read_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            id=validated_data['id'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            gender=validated_data.get('gender', ''),
            age=validated_data.get('age', ''),
            phone=validated_data.get('phone', ''),
            reason=validated_data.get('reason', '')
        )
        return user
