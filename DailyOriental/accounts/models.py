from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, id, password=None, **extra_fields):
        """
        Create and save a user with the given id and password.
        """
        if not id:
            raise ValueError('The ID field must be set')
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password=None, **extra_fields):
        """
        Create and save a superuser with the given id and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(id, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # username 필드를 사용하지 않음
    id = models.CharField(max_length=150, unique=True, primary_key=True, verbose_name="사용자 ID")
    password = models.CharField(max_length=200, verbose_name="이름")
    name = models.CharField(max_length=50, verbose_name="이름")
    gender = models.CharField(max_length=2, verbose_name="성별")
    age = models.CharField(max_length=10, verbose_name="나이")
    phone = models.CharField(max_length=13, verbose_name="번호")
    reason = models.CharField(max_length=20, verbose_name="가입사유")
    survey_result = models.CharField(max_length=10, blank=True, null=True, verbose_name="설문 결과")

    USERNAME_FIELD = 'id'  # 사용자 이름으로 id를 사용
    REQUIRED_FIELDS = ['name', 'gender', 'age', 'phone', 'reason']

    objects = CustomUserManager()

    def __str__(self):
        return self.id