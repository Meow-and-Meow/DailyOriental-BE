from django.conf import settings
from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    url_text = models.TextField()
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f'Notification for {self.user.id} = {self.user.name}: {self.message}'