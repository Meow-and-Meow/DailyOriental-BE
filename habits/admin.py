# habits/admin.py
from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'text', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('user__id', 'category', 'text')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')
