from django import forms
from .models import Student

# ================= STUDENT FORM ================================
class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        # Exclude auto-calculated fields from the form
        exclude = ["total_fee_paid", "total_fee_due"]
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "admission_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "address": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap class to all fields automatically
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-control"})

