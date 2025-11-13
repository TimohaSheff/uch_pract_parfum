from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('login', 'email', 'name', 'surname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Персональная информация', {'fields': ('name', 'surname', 'patronymic', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'email', 'name', 'surname', 'patronymic', 'password1', 'password2'),
        }),
    )
    search_fields = ('login', 'email', 'name', 'surname')
    ordering = ('-date_joined',)
    filter_horizontal = ()  # Убираем filter_horizontal, так как у нас нет groups и user_permissions

