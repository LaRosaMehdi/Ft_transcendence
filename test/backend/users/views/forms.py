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

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']
        if User.objects.filter(username=new_username).exists():
            raise forms.ValidationError("This username is already taken.")
        return new_username

class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['image']

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)
