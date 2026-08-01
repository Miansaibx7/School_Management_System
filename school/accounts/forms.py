from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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

# ================= Profile Form ===================================
class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "phone",
            "bio",
            "avatar",
        ]
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
        fields = [
            "name",
            "email",
            "phone",
            "bio",
            "avatar",
            "is_admin",
            "is_accountant",
            "is_staff",
            "is_active",
        ]

