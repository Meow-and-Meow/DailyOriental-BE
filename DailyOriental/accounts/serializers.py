from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'gender', 'age', 'phone', 'reason']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            age=validated_data['age'],
            phone=validated_data['phone'],
            reason=validated_data['reason'],
        )
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.reason = validated_data.get('reason', instance.reason)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
