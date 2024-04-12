from django import forms
from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

# User Registration
# -----------------

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, required=True)
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

# User Login
# ----------

class LoginForm(forms.Form):
    user_id = forms.CharField(label='Username or Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)

# Two Factor Authentication (2FA)
# --------------------------------

class TwoFactorForm(forms.Form):
    validation_code = forms.CharField(label='Validation Code', max_length=6, min_length=6)

    def clean_validation_code(self):
        validation_code = self.cleaned_data['validation_code']
        if not validation_code.isdigit() or len(validation_code) != 6:
            raise forms.ValidationError("Please enter a valid 6-digit code.")
        return validation_code