from django.contrib import admin
'''from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'gender', 'age_group', 'phone', 'signup_reason')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'gender', 'age_group', 'phone', 'signup_reason')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
'''