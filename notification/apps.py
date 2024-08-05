from django.apps import AppConfig
from django.conf import settings
import os

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'

    scheduler_started = False

    def ready(self):
        if settings.SCHEDULER_DEFAULT and not NotificationConfig.scheduler_started:
            from .tasks import scheduler
            if not scheduler.running:
                if os.environ.get('RUN_MAIN', None) != 'true':
                    scheduler.start()
                    NotificationConfig.scheduler_started = True
                    print("Scheduler started.")
            else:
                print("Scheduler is already running.")
        else:
            print("Scheduler configuration or state is not valid.")