from decimal import Decimal
from django.conf import settings

from django.core.validators import MinValueValidator  # Prevents negative Numbers
from django.db import models

from django.db.models import F, Q, Sum
# TruncMonth converts a date into the first day of its month
# Example: 2026-03-15 → 2026-03-01
from django.db.models.functions import Coalesce,TruncMonth # Coalesce to prevent 'None' values in charts
from django.utils import timezone


# ============================= EXPENSE/INCOME MODEL ======================================================================
class Transaction(models.Model):
    """General school transactions for profit/loss tracking"""

    TRANSACTION_TYPES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    CATEGORIES = (
        ("fee", "Student Fees"),
        ("salary", "Teacher Salaries"),
        ("utilities", "Utilities"),
        ("maintenance", "Maintenance"),
        ("supplies", "Supplies"),
        ("equipment", "Equipment"),
        ("rent", "Rent"),
        ("other_income", "Other Income"),
        ("other_expense", "Other Expense"),
    )
    # Short title describing the transaction
    title = models.CharField(max_length=200)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    receipt_number = models.CharField(max_length=50, blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            "-date",
            "-created_at",
        ]  # First order by latest transaction date, then by creation time
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["transaction_type"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.title} - ({self.get_transaction_type_display()}) {self.amount}"

    # Get monthly income vs expense for charts
    @classmethod
    def get_monthly_summary(cls, year=None):

        if not year:  # If year is not provided, use the current year
            year = timezone.now().year
            # This allows grouping transactions by month
        return (
            cls.objects.filter(date__year=year)
            .annotate(
                month=TruncMonth("date")  # TruncMonth converts a date
                # into the first day of its month Example: 2026-03-15 → 2026-03-01
                # Group results by the month field
            )
            .values("month")
            .annotate(
                # Added Coalesce so charts get '0' instead of 'None' if no data exists
                total_income=Coalesce(
                    Sum("amount", filter=Q(transaction_type="income")), Decimal("0.00")
                ),
                total_expense=Coalesce(
                    Sum("amount", filter=Q(transaction_type="expense")), Decimal("0.00")
                ),
            )
            .order_by("month")
        )  # Order results chronologically from January to December

    # Calculate total profit or loss for a given year
    @classmethod
    def get_yearly_profit(cls, year=None):

        if not year:
            year = timezone.now().year
        # Aggregate total income and expense in one query
        result = cls.objects.filter(date__year=year).aggregate(
            # Sum of all income transactions
            # Added Coalesce to prevent math errors on empty records
            total_income=Coalesce(
                Sum("amount", filter=Q(transaction_type="income")), Decimal("0.00")
            ),
            # Sum of all expense transactions
            total_expense=Coalesce(
                Sum("amount", filter=Q(transaction_type="expense")), Decimal("0.00")
            ),
        )
        # Handle None values if no transactions exist Return profit or loss
        return result["total_income"] - result["total_expense"]

    # Returns total transaction amount grouped by category.Useful for category-based charts.
    @classmethod
    def get_category_totals(cls):

        return (
            cls.objects.values("category")
            .annotate(
                # Sum of all transactions in each category
                total_amount=Sum("amount")
            )
            .order_by("-total_amount")
        )

    # Calculate monthly profit or loss for a given year.
    @classmethod
    def get_monthly_profit_loss(cls, year=None):

        if not year:
            year = timezone.now().year

        return (
            cls.objects.filter(date__year=year)
            .annotate(
                # Extract month from date
                month=TruncMonth(
                    "date"
                )  # TruncMonth converts a date into the first day of its month Example: 2026-03-15 → 2026-03-01
            )
            .values("month")
            .annotate(
                # Monthly income
                # Coalesced values to ensure profit calculation works
                total_income=Coalesce(
                    Sum("amount", filter=Q(transaction_type="income")), Decimal("0.00")
                ),
                # Monthly expense
                total_expense=Coalesce(
                    Sum("amount", filter=Q(transaction_type="expense")), Decimal("0.00")
                ),
            )
            .annotate(
                # F Use for the value from the database column when performing the calculation.
                profit=F("total_income")
                - F("total_expense")
                # Profit = income - expense
            )
            .order_by("month")
        )
