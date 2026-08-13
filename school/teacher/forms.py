from django import forms
from .models import Teacher

# ================= TEACHER FORM ======================================================
class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = "__all__"
        # We exclude calculated fields so users don't manually alter them on creation
        exclude = ["total_salary_paid", "salary_due"]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "date_of_joining": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
            "photo": forms.ClearableFileInput(attrs={"class": "file-upload"}),
            "subject_specialization": forms.TextInput(
                attrs={
                    "class": "tf-input-field",
                    "placeholder": "e.g. Mathematics, Physics",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

