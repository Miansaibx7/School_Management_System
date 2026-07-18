from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import (Teacher,
    Class,
    Section,
    Student,
    Transaction,
    Fee,
    Salary)

User = get_user_model()

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','name', 'password1','password2']

    def clean_password1(self):
         password = self.cleaned_data.get('password1')

         if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")

         if not any(char.isdigit() for char in password):
              raise forms.ValidationError("Password must contain at least one number.")

         return password

# ================= Profile Form ===================================
class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["name","email","phone","bio","avatar",]

        widgets = { 
                "name": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter your full name",}),
                "email": forms.EmailInput(attrs={ "class": "form-control", "placeholder": "Enter email address",}),
                "phone": forms.TextInput(attrs={ "class": "form-control", "placeholder": "Enter phone number",}),
                "bio": forms.Textarea(attrs={ "class": "form-control", "rows": 4, "placeholder": "Write something about yourself...",}),
            }
  

# ================= USER FORM ======================================
class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["name", "email", "phone", "bio", "avatar",
            "is_admin", "is_accountant", "is_staff","is_active",]


# ================= TEACHER FORM ======================================================
class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = "__all__"
        # We exclude calculated fields so users don't manually alter them on creation
        exclude = ['total_salary_paid', 'salary_due'] 
        
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'photo': forms.ClearableFileInput(attrs={'class': 'file-upload'}),
            'subject_specialization': forms.TextInput(attrs={
                'class': 'tf-input-field', 
                'placeholder': 'e.g. Mathematics, Physics',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ================= CLASS FORM =========================================================
class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = "__all__"
        
        # Injects Bootstrap classes and our custom animation classes into the HTML.
        widgets = {
            'name': forms.Select(attrs={'class': 'form-select custom-input-anim',}),
            'monthly_fee': forms.NumberInput(attrs={'class': 'form-control custom-input-anim',
                'placeholder': 'Enter monthly fee (e.g. 5000.00)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input custom-check-anim',}),
            
            # If you add a teacher ForeignKey to your model later, the widget would look like this:
            # 'class_teacher': forms.Select(attrs={'class': 'form-select custom-input-anim'}),
        }

# ================= SECTION FORM =====================================
class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., A, B, C'}),
            'student_class': forms.Select(attrs={'class': 'form-select'}),
            'class_teacher': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'})
        }


# =============================== STUDENT FORM =====================================================
class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        # Exclude auto-calculated fields from the form
        exclude = ['total_fee_paid', 'total_fee_due']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap class to all fields automatically
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})


# ============================= TRANSACTION FORM ==============================================
class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        # Exclude 'recorded_by' so users don't set it manually
        exclude = ['recorded_by'] 
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap class 'form-control' or 'form-select' to all fields automatically
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})
                
        # Select dropdowns to use the correct Bootstrap class
        self.fields['transaction_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['category'].widget.attrs.update({'class': 'form-select'})


# ================================ FEE FORM ==================================================
class FeeForm(forms.ModelForm):

    class Meta:
        model = Fee
        # Also exclude 'received_by' because we set it automatically in the view
        exclude = ["transaction", "created_at", "received_by"]
        widgets = {
            'month_for': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


# ================================== SALARY FORM ===================================================
class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        # Also exclude 'paid_by' because we set it automatically in the view
        exclude = ["transaction", "created_at", "updated_at", "paid_by"]
        widgets = {
            'month_for': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'bank_reference': forms.TextInput(attrs={'class': 'form-control',
                'placeholder': 'Enter bank transaction ID / reference'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})