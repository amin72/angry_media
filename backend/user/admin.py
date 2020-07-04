from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff']
    search_fields = ['username', 'email']
    readonly_fields = ['last_login', 'date_joined', 'password']
