# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'password')}),
        ('Personal info', {'fields': ('name', 'gender', 'age', 'phone', 'reason')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'name', 'is_staff')
    search_fields = ('id', 'name')
    ordering = ('id',)

admin.site.register(CustomUser, CustomUserAdmin)
