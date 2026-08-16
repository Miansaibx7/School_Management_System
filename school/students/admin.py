from django.contrib import admin
from .models import  Student

# ==================== Student Admin ====================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "admission_number",
        "class_room",
        "section",
        "roll_number",
        "is_active",
    )
    search_fields = (
        "first_name",
        "last_name",
        "admission_number",
        "phone_number",
        "email",
    )
    list_filter = ("class_room", "section", "gender", "is_active")
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "father_name",
                    "mother_name",
                    "gender",
                    "date_of_birth",
                    "blood_group",
                    "photo",
                )
            },
        ),
        (
            "Academic",
            {
                "fields": (
                    "admission_number",
                    "roll_number",
                    "class_room",
                    "section",
                    "admission_date",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "phone_number",
                    "guardian_name",
                    "guardian_phone",
                    "email",
                    "address",
                )
            },
        ),
        ("Fee Summary", {"fields": ("total_fee_paid", "total_fee_due")}),
        ("Status", {"fields": ("is_active", "user", "created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at", "total_fee_paid", "total_fee_due")
