from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Custom User Fields',
            {
                'fields': (
                    'member_type',
                    'is_deleted',
                ),
            },
        ),
    )
