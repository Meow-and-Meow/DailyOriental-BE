# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('남', '남성'),
        ('여', '여성'),
    )
    AGE_CHOICES = (
        ('10s', '10대'),
        ('20s', '20대'),
        ('30s', '30대'),
        ('40s', '40대'),
        ('50s', '50대'),
        ('60s', '60대'),
        ('70+', '70대 이상'),
    )
    REASON_CHOICES = (
        ('interest', '한방에 대한 관심'),
        ('self_diagnosis', '사상체질 자가진단'),
        ('habit', '건강 습관 개선'),
        ('knowledge', '건강 상식 획득'),
        ('recommendation', '지인 추천'),
        ('other', '기타'),
    )
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age_group = models.CharField(max_length=3, choices=AGE_CHOICES)
    phone = models.CharField(max_length=13)
    signup_reason = models.CharField(max_length=20, choices=REASON_CHOICES)

    def __str__(self):
        return self.username
