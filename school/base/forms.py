from django import forms

from .models import Fee, Salary, Student, Transaction

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


# ================= TRANSACTION FORM ===================================
class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        # Exclude 'recorded_by' so users don't set it manually
        exclude = ["recorded_by"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap class 'form-control' or 'form-select' to all fields automatically
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-control"})

        # Fix for Select dropdowns to use the correct Bootstrap class
        self.fields["transaction_type"].widget.attrs.update({"class": "form-select"})
        self.fields["category"].widget.attrs.update({"class": "form-select"})


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
