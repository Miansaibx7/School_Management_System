from django.contrib import admin

from .models import Fee, Salary, Section, Student, Transaction

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


# ==================== Transaction Admin ====================
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "transaction_type",
        "category",
        "amount",
        "date",
        "recorded_by",
    )
    search_fields = ("title", "description", "receipt_number")
    list_filter = ("transaction_type", "category", "date")
    ordering = ("-date",)


# ==================== Fee Admin ====================
@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "amount",
        "month_for",
        "status",
        "payment_date",
        "payment_method",
    )
    search_fields = ("student__first_name", "student__last_name", "notes")
    list_filter = ("status", "payment_method", "payment_date")
    ordering = ("-payment_date",)


# ==================== Salary Admin ====================
@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "amount",
        "month_for",
        "status",
        "payment_date",
        "payment_method",
    )
    search_fields = ("teacher__first_name", "teacher__last_name", "bank_reference")
    list_filter = ("status", "payment_method", "payment_date")
    ordering = ("-payment_date",)


# Optional: if you still want to use admin.site.register, do it only once:
# admin.site.register(User, UserAdmin)  # NOT needed if you used the decorator
