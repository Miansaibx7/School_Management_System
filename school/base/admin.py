from django.contrib import admin
from .models import Salary

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
