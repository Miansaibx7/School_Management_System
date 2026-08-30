from django.conf import settings
from teacher.models import Teacher
from transaction.models import Transaction

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator  # Prevents negative Numbers
from django.db import models, transaction as db_transaction  # Use alias to prevent naming conflicts

from django.utils import timezone

# =============================== SALARY MODEL =============================================================
class Salary(models.Model):
    """Teacher salary payment records"""

    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("bank", "Bank Transfer"),
        ("check", "Check")
    )

    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled")
    )
    # One Teacher can have Multiple monthly Salary payments
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="salary_payments")

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="salary_record",
        null=True,
        blank=True
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    month_for = models.DateField(help_text="Salary for which month/year", db_index=True)
    payment_date = models.DateField(default=timezone.now, db_index=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="bank")
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
                name="unique_teacher_salary_month"
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

        with (db_transaction.atomic()):# Ensure salary save and teacher salary status update happen in a single database transaction

            # Check transaction_id to safely see if the relationship exists yet
            # Logic now updates the existing transaction if the Salary is edited
            transaction_data = {
                "title": f"Salary Payment - {self.teacher.full_name}",
                "transaction_type": "expense",
                "category": "salary",
                "amount": self.amount,
                "date": self.payment_date,
                "recorded_by": self.paid_by,
            }

            if self.transaction:
                # Updates the expense record if salary amount/date changes
                Transaction.objects.filter(id=self.transaction.id).update(**transaction_data)
            else:
                new_trans = Transaction.objects.create(**transaction_data)
                self.transaction = new_trans

            super().save(*args, **kwargs)
            if hasattr(self.teacher, "update_salary_status"):
                self.teacher.update_salary_status()  # Update salary status on the related teacher model