from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('mood', '기분'),
    ('exercise', '운동'),
    ('happiness', '행복'),
    ('diet', '식습관'),
]

DEFAULT_HABITS = {
    'mood': [
        "10분 동안 명상하기",
        "감사한 일 3가지 적어보기",
        "좋아하는 노래 3곡 듣기",
        "10분 동안 하늘 쳐다보기",
        "가까운 친구와 가족에게 안부 메세지 보내기",
        "저녁식사 후 따뜻한 차 한 잔 마시기",
        "영화 한 편 보기",
        "큰 소리로 3번 웃기 “하하하”",
        "자화상 그려보기",
    ],
    'exercise': [
        "집 주변 30분 걷기",
        "스트레칭 10분 하기",
        "짧은 홈트레이닝(스쿼트, 팔굽혀펴기 등) 10분 하기",
        "계단 오르내리기",
        "점심시간 후 10분 산책하기",
        "자기 전에 간단한 스트레칭하기",
        "스쿼트 20개 하기",
    ],
    'diet': [
        "하루동안 물 8잔 마시기",
        "제철 과일 챙겨 먹기",
        "인스턴트 음식 먹지 않기",
        "정해진 시간에 식사하기",
        "식사 중 휴대폰 또는 TV 보지 않기",
        "가공식품 대신 자연식품 먹기",
    ],
    'happiness': [
        "오늘 잘한 일 3가지 생각해보기",
        "나의 강점 5가지 적기",
        "오늘 배운 새로운 것 3가지",
        "좋아하는 사진 찍기",
        "스스로에게 선물하기",
        "성취 리스트 3가지 적기",
        "기쁜 순간 3가지 적어보기",
        "나의 예쁜 점 3가지 적기",
    ],
}

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=True)  # default 필드 추가

    def __str__(self):
        return f"{self.user.id} - {self.category} - {self.text}"
