from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Log


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """カスタムユーザー管理画面"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('個人情報', {'fields': ('first_name', 'last_name', 'email')}),
        ('権限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要な日付', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """ログ管理画面"""
    list_display = ('date', 'text', 'id')
    list_filter = ('date',)
    search_fields = ('text',)
    ordering = ('-date',)
