from django import forms
from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

# User Settings
# -------------

class ChangeUsernameForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['username'].max_length = 20  # Set max length for the username field
        self.fields['username'].widget.attrs['maxlength'] = '20'  # HTML attribute for max length

    def clean_username(self):
        new_username = self.cleaned_data.get('username')
        if new_username and len(new_username) > 20:
            raise forms.ValidationError("Username cannot exceed 20 characters.")
        if User.objects.filter(username=new_username).exists():
            raise forms.ValidationError("This username is already taken.")
        return new_username


class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['image']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'maxlength': 30}),
        required=True
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'maxlength': 30}),
        required=True
    )
    confirm_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'maxlength': 30}),
        required=True
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if old_password and len(old_password) > 30:
            raise forms.ValidationError("Old password cannot exceed 30 characters.")
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password and len(new_password) > 30:
            raise forms.ValidationError("New password cannot exceed 30 characters.")
        return new_password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password and len(confirm_password) > 30:
            raise forms.ValidationError("Confirm password cannot exceed 30 characters.")
        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'New password and confirmation do not match.')

class Change2faForm(forms.Form):
    enable_2fa = forms.BooleanField(label='Enable 2FA', required=False, widget=forms.CheckboxInput)