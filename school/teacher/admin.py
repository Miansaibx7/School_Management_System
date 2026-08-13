from django.contrib import admin
from .models import Teacher

# ==================== Teacher Admin ====================
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "teacher_id",
        "designation",
        "phone_number",
        "is_active",
    )
    search_fields = ("first_name", "last_name", "teacher_id", "email", "phone_number")
    list_filter = ("designation", "gender", "is_active")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "gender", "date_of_birth", "photo")},
        ),
        (
            "Professional Information",
            {
                "fields": (
                    "teacher_id",
                    "qualification",
                    "subject_specialization",
                    "designation",
                    "date_of_joining",
                )
            },
        ),
        (
            "Contact",
            {"fields": ("phone_number", "email", "address", "emergency_contact")},
        ),
        (
            "Salary & Bank",
            {
                "fields": (
                    "monthly_salary",
                    "total_salary_paid",
                    "salary_due",
                    "bank_name",
                    "account_number",
                    "ifsc_code",
                )
            },
        ),
        (
            "Status & Timestamps",
            {"fields": ("is_active", "user", "created_at", "updated_at")},
        ),
    )
    readonly_fields = ("created_at", "updated_at", "total_salary_paid", "salary_due")