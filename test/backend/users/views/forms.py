from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

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

class LoginForm(forms.Form):
    user_id = forms.CharField(label='Username or Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)