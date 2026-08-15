from django.contrib import admin

from .models import Section

# ==================== Section Admin ====================
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "student_class",
        "name",
        "class_teacher",
        "capacity",
        "student_count",
        "is_active",
    )
    search_fields = ("name",)
    list_filter = ("student_class", "is_active")
    ordering = ("student_class", "name")
    readonly_fields = ("student_count", "available_seats")

