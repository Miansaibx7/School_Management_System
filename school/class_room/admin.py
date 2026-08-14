from django.contrib import admin

from .models import Class


# ==================== Class Admin ====================
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("name", "monthly_fee", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
