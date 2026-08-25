from django.conf import settings
from students.models import Student
from transaction.models import Transaction

from django.core.validators import MinValueValidator  # Prevents negative Numbers
from django.db import models, transaction as db_transaction  # Use alias to prevent naming conflicts

from django.utils import timezone

# ================================== FEE MODEL ===================================================
class Fee(models.Model):
    """Student fee payment records"""
    
    PAYMENT_METHODS = (
        ("cash", "Cash"),
        ("bank", "Bank Transfer"),
        ("check", "Check"),
        ("online", "Online Payment")
    )

    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("partial", "Partial")
    )

    # One student can have multiple monthly fee payments
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fee_payments")
    
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="fee_record",
        null=True,
        blank=True,
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="paid")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    month_for = models.DateField(help_text="Fee for which month/year", db_index=True)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="cash")
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
        with (db_transaction.atomic()):# Ensure fee save and student fee status update happen in a single database transaction

            # ( Use the aliased db_transaction )
            # Check transaction_id to safely see if the relationship exists yet
            # Logic now updates the existing transaction if the Fee is edited
            transaction_data = {
                "title": f"Fee Payment - {self.student.full_name}",
                "transaction_type": "income",
                "category": "fee",
                "amount": self.amount,
                "date": self.payment_date,
                "recorded_by": self.received_by,
            }

            if self.transaction:
                # This ensures that if you change the Fee amount, the Transaction record also updates
                Transaction.objects.filter(id=self.transaction.id).update(**transaction_data)
            else:
                new_trans = Transaction.objects.create(**transaction_data)
                self.transaction = new_trans

            super().save(*args, **kwargs)

            # Use hasattr to ensure the student actually has this method
            if hasattr(self.student, "update_fee_status"):
                self.student.update_fee_status()