from django.contrib import admin
from .models import Transaction


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