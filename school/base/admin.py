from django.contrib import admin

from .models import Fee, Salary, Transaction

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
