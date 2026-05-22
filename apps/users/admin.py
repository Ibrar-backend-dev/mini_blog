from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_email_verified')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Verification Status', {'fields': ('is_email_verified',)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('is_email_verified',)}),
    )
    