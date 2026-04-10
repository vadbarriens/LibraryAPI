from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для отображения модели в админке"""
    list_display = ('id', 'email')
