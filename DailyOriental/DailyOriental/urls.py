from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # accounts 앱의 URL 포함
    path('accounts/', include('accounts.urls')), 
]
