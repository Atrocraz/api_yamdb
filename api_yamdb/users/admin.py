from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets+(
        ('Права доступа API',
            {'fields': ('role',), },
         ),
    )
