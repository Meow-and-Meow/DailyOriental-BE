from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'name', 'gender', 'age_group', 'phone', 'signup_reason')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            **validated_data
        )
        return user

class SocialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'gender', 'age_group', 'phone', 'signup_reason']

    def validate_gender(self, value):
        if value not in ['남', '여']:
            raise serializers.ValidationError("Gender must be either '남' or '여'.")
        return value
