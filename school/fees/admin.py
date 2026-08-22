from django.contrib import admin
from .models import Fee

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