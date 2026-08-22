from django import forms
from .models import Fee

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
