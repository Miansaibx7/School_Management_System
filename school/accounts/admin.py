from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# Register your models here.
# ==================== User Admin ====================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "name", "role", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser", "is_admin", "is_accountant")
    search_fields = ("email", "name", "phone")
    ordering = ("-date_joined",)
    fieldsets = BaseUserAdmin.fieldsets + (  # merges default fieldsets
        (
            "Additional Info",
            {"fields": ("phone", "bio", "avatar", "is_admin", "is_accountant")},
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "email",
                    "name",
                    "phone",
                    "bio",
                    "avatar",
                    "is_admin",
                    "is_accountant",
                )
            },
        ),
    )
