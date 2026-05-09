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
        fields = ['email','name', 'password1', 'password2']

    def clean_password1(self):
         password = self.cleaned_data.get('password1')

         if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters.")

         if not any(char.isdigit() for char in password):
              raise forms.ValidationError("Password must contain at least one number.")

         return password
     
     

# ================= USER FORM =================
class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "phone",
            "bio",
            "avatar",
            "is_admin",
            "is_accountant"
        ]


# ================= TEACHER FORM =================
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
        }


# ================= CLASS FORM =================
class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = "__all__"
        
        # This injects Bootstrap classes and our custom animation classes into the HTML.
        widgets = {
            'name': forms.Select(attrs={'class': 'form-select custom-input-anim',}),
            'monthly_fee': forms.NumberInput(attrs={'class': 'form-control custom-input-anim',
                'placeholder': 'Enter monthly fee (e.g. 5000.00)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input custom-check-anim',}),
            
            # If you add a teacher ForeignKey to your model later, the widget would look like this:
            # 'class_teacher': forms.Select(attrs={'class': 'form-select custom-input-anim'}),
        }

# ================= SECTION FORM =================
class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = "__all__"


# ================= STUDENT FORM =================
class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = "__all__"


# ================= TRANSACTION FORM =================
class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = "__all__"


# ================= FEE FORM =================
class FeeForm(forms.ModelForm):

    class Meta:
        model = Fee
        exclude = ["transaction", "created_at"]


# ================= SALARY FORM =================
class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        exclude = ["transaction", "created_at", "updated_at"]