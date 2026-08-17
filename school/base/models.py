from decimal import Decimal

from django.conf import settings
from teacher.models import Teacher
from students.models import Student

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator  # Prevents negative Numbers
from django.db import models, transaction as db_transaction  # Use alias to prevent naming conflicts

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
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
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
                # FIXED: Added Coalesce so charts get '0' instead of 'None' if no data exists
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
            # FIXED: Added Coalesce to prevent math errors on empty records
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
                # FIXED: Coalesced values to ensure profit calculation works
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


# ======================= FEE MODEL =======================================================================================
class Fee(models.Model):
    """Student fee payment records"""

    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("bank", "Bank Transfer"),
        ("check", "Check"),
        ("online", "Online Payment"),
    )

    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("partial", "Partial"),
    )

    # One student can have multiple monthly fee payments
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="fee_payments"
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="fee_record",
        null=True,
        blank=True,
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="paid")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    month_for = models.DateField(help_text="Fee for which month/year", db_index=True)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, default="cash"
    )
    notes = models.TextField(blank=True)

    # Staff member who received the payment
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_fees",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "month_for"], name="unique_student_fee_month"
            )
        ]
        verbose_name = "Fee Payment"
        verbose_name_plural = "Fee Payments"

    def __str__(self):
        return f"{self.student.full_name} - {self.amount} ({self.month_for.strftime('%B %Y')})"

    def save(self, *args, **kwargs):
        with (
            db_transaction.atomic()
        ):  # Ensure fee save and student fee status update happen in a single database transaction
            # ( Use the aliased db_transaction )
            # Check transaction_id to safely see if the relationship exists yet
            # CHANGED: Logic now updates the existing transaction if the Fee is edited
            transaction_data = {
                "title": f"Fee Payment - {self.student.full_name}",
                "transaction_type": "income",
                "category": "fee",
                "amount": self.amount,
                "date": self.payment_date,
                "recorded_by": self.received_by,
            }

            if self.transaction:
                # FIXED: This ensures that if you change the Fee amount, the Transaction record also updates
                Transaction.objects.filter(id=self.transaction.id).update(
                    **transaction_data
                )
            else:
                new_trans = Transaction.objects.create(**transaction_data)
                self.transaction = new_trans

            super().save(*args, **kwargs)

            # Use hasattr to ensure the student actually has this method
            if hasattr(self.student, "update_fee_status"):
                self.student.update_fee_status()


# ========================== SALARY MODEL ================================================================================
class Salary(models.Model):
    """Teacher salary payment records"""

    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("bank", "Bank Transfer"),
        ("check", "Check"),
    )

    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled"),
    )
    # One Teacher can have multiple monthly Salary payments
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="salary_payments"
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="salary_record",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    month_for = models.DateField(help_text="Salary for which month/year", db_index=True)
    payment_date = models.DateField(default=timezone.now, db_index=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, default="bank"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    bank_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    # User (admin/accountant) who recorded the payment
    # If the user is deleted, the field will become NULL
    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="salary_payments_recorded",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-payment_date", "-month_for"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "teacher",
                    "month_for",
                ],  # Prevent duplicate salary records for the same teacher and month
                name="unique_teacher_salary_month",
            )
        ]
        verbose_name = "Salary Payment"
        verbose_name_plural = "Salary Payments"

    def __str__(self):
        return f"{self.teacher.full_name} - {self.amount} ({self.month_for.strftime('%B %Y')})"

    # Custom validation logic before saving the model.
    def clean(self):
        super().clean()

        # Ensure salary amount is greater than zero
        if self.amount <= 0:
            raise ValidationError("Salary must be greater than zero.")

        # Require transaction ID if payment method is bank transfer
        # Changed self.transaction_id to self.bank_reference
        if self.payment_method == "bank" and not self.bank_reference:
            raise ValidationError("Bank Reference required for bank payments.")

    def save(self, *args, **kwargs):
        # Forces validation to run even when saving via script (not just forms)
        self.full_clean()

        with (
            db_transaction.atomic()
        ):  # Ensure salary save and teacher salary status update happen in a single database transaction
            # Check transaction_id to safely see if the relationship exists yet
            # CHANGED: Logic now updates the existing transaction if the Salary is edited
            transaction_data = {
                "title": f"Salary Payment - {self.teacher.full_name}",
                "transaction_type": "expense",
                "category": "salary",
                "amount": self.amount,
                "date": self.payment_date,
                "recorded_by": self.paid_by,
            }

            if self.transaction:
                # FIXED: Updates the expense record if salary amount/date changes
                Transaction.objects.filter(id=self.transaction.id).update(
                    **transaction_data
                )
            else:
                new_trans = Transaction.objects.create(**transaction_data)
                self.transaction = new_trans

            super().save(*args, **kwargs)
            if hasattr(self.teacher, "update_salary_status"):
                self.teacher.update_salary_status()  # Update salary status on the related teacher model
