from django import forms
from .models import Section

# ================= SECTION FORM =====================================
class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., A, B, C"}
            ),
            "student_class": forms.Select(attrs={"class": "form-select"}),
            "class_teacher": forms.Select(attrs={"class": "form-select"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
        }

