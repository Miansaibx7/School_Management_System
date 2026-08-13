from django.db import models

from dateutil.relativedelta import relativedelta
from django.conf import settings

from django.core.validators import MinValueValidator  # Prevents negative Numbers

from django.utils import timezone
from decimal import Decimal

from django.db.models import Sum


class Teacher(models.Model):
    """Complete Teacher model with salary tracking"""

    GENDER_CHOICES = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))
    DESIGNATIONS = (
        ("Principal", "Principal"),
        ("Vice Principal", "Vice Principal"),
        ("HOD", "Head of Department"),
        ("Senior Teacher", "Senior Teacher"),
        ("Teacher", "Teacher"),
        ("Assistant Teacher", "Assistant Teacher"),
    )
    # Link to User model (for portal access to the teacher if the admin want )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teacher_profile",
    )

    # Fully delete the data of a user each and every thing
    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)

    # Professional ID
    teacher_id = models.CharField(max_length=20, unique=True, db_index=True)
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="teachers/", blank=True, null=True)
    # Professional Information
    qualification = models.CharField(max_length=200, blank=True)
    subject_specialization = models.CharField(max_length=200, blank=True)
    designation = models.CharField(
        max_length=50, choices=DESIGNATIONS, default="Teacher"
    )
    date_of_joining = models.DateField()
    # Contact Information
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    # Salary Information
    monthly_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )
    total_salary_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    salary_due = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    # Bank Details (for salary transfer)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    # Status
    is_active = models.BooleanField(default=True)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_salary_status(self):
        """Recalculate salary totals based on Salary records"""
         
        from base.models import Salary
        
        total = Salary.objects.filter(teacher=self).aggregate(total=Sum("amount"))[
            "total"
        ] or Decimal("0.00")
        self.total_salary_paid = total
        # Calculate expected salary based on months since joining
        months = self.calculate_months_since_joining()
        expected = self.monthly_salary * months
        self.salary_due = expected - self.total_salary_paid
        # Use update() to avoid triggering signals/recursion
        self.__class__.objects.filter(pk=self.pk).update(
            total_salary_paid=self.total_salary_paid, salary_due=self.salary_due
        )

    # Use for when every the teacher is joining the school and their salary calculation
    def calculate_months_since_joining(self):
        """Calculate months employed for salary calculation"""
        today = timezone.now().date()
        diff = relativedelta(today, self.date_of_joining)
        return diff.months + (diff.years * 12) + 1
