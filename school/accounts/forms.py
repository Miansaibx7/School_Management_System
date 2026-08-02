from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','name', 'password1', 'password2']

    def clean_email(self):
            email = self.cleaned_data.get('email', '').strip().lower()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this email already exists.")
            return email
    
    def clean_password1(self):
            password = self.cleaned_data.get('password1')
    
            if len(password) < 6:
                raise forms.ValidationError("Password must be at least 6 characters.")
    
            if not any(char.isdigit() for char in password):
                raise forms.ValidationError("Password must contain at least one number.")
    
            return password


# ================= Profile Form (self-service, NO role/permission fields) ===================
class ProfileForm(forms.ModelForm):
    """ Used by the logged-in user to edit their OWN profile.Deliberately excludes is_admin/is_accountant/is_staff/is_active —
    a user must never be able to grant themselves privileges through this form. """

    class Meta:
        model = User
        fields = ["name", "email", "phone", "bio", "avatar"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone number"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Write something about yourself..."}),
        }
  

# ================= USER FORM (admin-only — enforced in views.py via @admin_required) =========
class UserForm(forms.ModelForm):
    """Full user-management form including role/permission flags.
    SECURITY: any view using this form MUST be wrapped in @admin_required.
    Do not reuse this form for self-service profile editing — use ProfileForm."""

    class Meta:
        model = User
        fields = [
            "name", "email", "phone", "bio", "avatar",
            "is_admin", "is_accountant", "is_staff", "is_active",
        ]
