from decimal import Decimal
from dateutil.relativedelta import relativedelta

from django.conf import settings
from class_room.models import Class
from section.models import Section

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator  # Prevents negative Numbers
from django.db import models # Use alias to prevent naming conflicts

from django.db.models import  Sum
from django.utils import timezone

# ========================== STUDENT MODEL =================================================================================
class Student(models.Model):
    """Student model for School Management System"""

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    BLOOD_GROUP_CHOICES = (
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    )

    # Link to User model (optional - for portal access)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile",
    )
    # Personal Information of a Student
    photo = models.ImageField(upload_to="students/", blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    blood_group = models.CharField(
        max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True
    )
    # Academic Information of a Student
    admission_number = models.CharField(max_length=20, unique=True, db_index=True)
    roll_number = models.PositiveIntegerField(
        db_index=True, validators=[MinValueValidator(1)]
    )

    # One Class can have many Students (ForeignKey relationship)
    class_room = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="students"
    )

    # One Section can have many Students (One-to-Many relationship)
    section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    admission_date = models.DateField(default=timezone.localdate)
    # Contact Information
    phone_number = models.CharField(max_length=15, blank=True, db_index=True)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True, db_index=True)
    address = models.TextField()
    # Fee Summary Fields (auto-calculated)
    total_fee_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Auto-calculated from fee payments",
    )
    total_fee_due = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Auto-calculated based on months enrolled",
    )
    # Status
    is_active = models.BooleanField(default=True)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "class_room",
                    "section",
                    "roll_number",
                ],  # No duplicate roll numbers in same class
                name="unique_roll_per_section",
            )
        ]
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def clean(self):
        """Ensure that the selected section belongs to the selected class."""
        if self.section and self.section.student_class != self.class_room:
            raise ValidationError(
                {"section": "The selected section does not belong to the chosen class."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def update_fee_status(self):
        """Update fee status - calculate total paid and due amounts"""
        # Calculate total fees paid by student
        from base.models import Fee
        
        total_paid = Fee.objects.filter(student=self).aggregate(total=Sum("amount"))[
            "total"
        ] or Decimal("0.00")

        # Calculate expected fee based on months since admission
        months_enrolled = self.calculate_months_since_admission()
        monthly_fee = self.class_room.monthly_fee
        total_expected = monthly_fee * months_enrolled

        # Calculate amount due
        total_due = total_expected - total_paid

        # Update fields using update() to avoid recursion
        self.__class__.objects.filter(pk=self.pk).update(
            total_fee_paid=total_paid, total_fee_due=max(total_due, Decimal("0.00"))
        )

    def calculate_months_since_admission(self):
        """Calculate months since admission for fee calculation"""
        today = timezone.now().date()
        diff = relativedelta(today, self.admission_date)
        return diff.months + (diff.years * 12) + 1

    # String Representation
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"

    @property
    def full_name(self):
        """Returns student's full name"""
        return f"{self.first_name} {self.last_name}"

