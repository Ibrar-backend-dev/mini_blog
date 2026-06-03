from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_email_verified')
    
    readonly_fields = ('is_email_verified',)
    