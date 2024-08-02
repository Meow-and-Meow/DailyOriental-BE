from rest_framework import serializers
from .models import CustomUser
import string
import random

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'name', 'gender', 'age', 'phone', 'reason', 'survey_result', 'is_member')
        extra_kwargs = {
            'password': {'write_only': True},
            'survey_result': {'read_only': True},
            'is_member': {'read_only': True},
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

class GuestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'is_member')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'is_member': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['name'] = '여홍이'
        validated_data['is_member'] = False
        validated_data['id'] = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return super().create(validated_data)
