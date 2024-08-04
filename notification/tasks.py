from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Notification
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def send_daily_mission_notifications():
    now = timezone.now()
    users = User.objects.all()
    for user in users:
        message = "오늘의 미션을 완료했는지 확인해 보세요!"
        url_text = "미션 확인하러 가기"
        Notification.objects.create(user=user, message=message, url_text = url_text)

def send_health_tip_notifications():
    now = timezone.now()
    users = User.objects.all()
    for user in users:
        message = "AI 허준 건강 상식을 확인해 보세요!"
        url_text = "AI 허준에게 건강 상식 물어보기"
        Notification.objects.create(user=user, message=message, url_text = url_text)

def send_acupressure_point_notifications():
    now = timezone.now()
    users = User.objects.all()
    for user in users:
        message = "오늘의 지압점을 확인해 보세요!"
        url_text = "손 지압점 확인하러 가기"
        Notification.objects.create(user=user, message=message, url_text = url_text)

scheduler = BackgroundScheduler()

scheduler.add_job(send_daily_mission_notifications, 'interval',  days=1, start_date='2024-08-04 00:21:00', id='daily_mission')
scheduler.add_job(send_health_tip_notifications, 'interval', hours=12, start_date='2024-08-04 00:08:00', id='health_tip')
scheduler.add_job(send_acupressure_point_notifications, 'interval', hours=12, start_date='2024-08-04 00:08:00', id='acupressure_point')
