from django import forms
from .models import Fee, Salary

# ================= FEE FORM ==================================================
class FeeForm(forms.ModelForm):

    class Meta:
        model = Fee
        # Also exclude 'received_by' because we set it automatically in the view
        exclude = ["transaction", "created_at", "received_by"]
        widgets = {
            "month_for": forms.DateInput(attrs={"type": "date"}),
            "payment_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }



# ================= SALARY FORM ===================================================
class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        # Also exclude 'paid_by' because we set it automatically in the view
        exclude = ["transaction", "created_at", "updated_at", "paid_by"]
        widgets = {
            "month_for": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "payment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "bank_reference": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter bank transaction ID / reference",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-control"})
