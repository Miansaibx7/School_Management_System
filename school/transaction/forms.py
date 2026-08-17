from django import forms
from .models import Transaction

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

        # Select dropdowns to use the correct Bootstrap class
        self.fields["transaction_type"].widget.attrs.update({"class": "form-select"})
        self.fields["category"].widget.attrs.update({"class": "form-select"})