from teacher.models import Teacher
from class_room.models import Class

from django.core.validators import MinValueValidator  # Prevents negative Numbers
from django.db import models

from django.db.models import Q

# =============================== SECTION MODEL ==============================================================================
class Section(models.Model):
    """Model for class sections (A, B, C...)"""

    name = models.CharField(max_length=5, default="A")
    # One Class can have many Sections (ForeignKey relationship)
    student_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="sections"
    )

    # One Teacher can be assigned to one Section (ForeignKey relationship)
    class_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="section_teacher",
    )

    capacity = models.PositiveIntegerField(
        default=40, validators=[MinValueValidator(1)]
    )
    # Status
    is_active = models.BooleanField(default=True)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "student_class",
            "name",
        ]
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        # Merged constraints into a single list for better readability and performance

    constraints = [
        models.UniqueConstraint(
            fields=["student_class", "name"],  # No duplicate class-section combos
            name="unique_class_section",
        ),
        models.UniqueConstraint(
            fields=["class_teacher"],
            condition=Q(class_teacher__isnull=False),
            name="unique_class_teacher",
        ),
    ]

    def __str__(self):
        return f"{self.student_class.name} - {self.name}"

    @property
    def student_count(self):
        return self.students.count()

    @property
    def available_seats(self):
        return self.capacity - self.student_count