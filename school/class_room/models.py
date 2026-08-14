from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator  # Prevents negative Numbers

# ======================== CLASS MODEL ================================================================================
class Class(models.Model):
    """Model for school classes/grades"""

    CLASS_CHOICES = [
        ("Nursery", "Nursery"),
        ("Class 1", "Class 1"),
        ("Class 2", "Class 2"),
        ("Class 3", "Class 3"),
        ("Class 4", "Class 4"),
        ("Class 5", "Class 5"),
        ("Class 6", "Class 6"),
        ("Class 7", "Class 7"),
        ("Class 8", "Class 8"),
        ("Class 9", "Class 9"),
        ("Class 10", "Class 10"),
        ("Class 11", "Class 11"),
        ("Class 12", "Class 12"),
    ]
    # Class Information
    name = models.CharField(
        max_length=20, choices=CLASS_CHOICES, db_index=True, unique=True
    )
    # Fee Structure
    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )
    # Status
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]  # sort alphabetically (Class 1, Class 2).
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name
