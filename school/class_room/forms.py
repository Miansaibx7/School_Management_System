from django import forms
from .models import Class

# ================= CLASS FORM =========================================================
class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = "__all__"

        # This injects Bootstrap classes and our custom animation classes into the HTML.
        widgets = {
            "name": forms.Select(
                attrs={
                    "class": "form-select custom-input-anim",
                }
            ),
            "monthly_fee": forms.NumberInput(
                attrs={
                    "class": "form-control custom-input-anim",
                    "placeholder": "Enter monthly fee (e.g. 5000.00)",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input custom-check-anim",
                }
            ),
            # If you add a teacher ForeignKey to your model later, the widget would look like this:
            # 'class_teacher': forms.Select(attrs={'class': 'form-select custom-input-anim'}),
        }
