import requests, re, logging
from requests import get
from users.models import User
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from users.views import *

logger = logging.getLogger(__name__)

# SETTINGS
# --------

@login_required
def setting_change_username(request):
    errors = []
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            if User.objects.filter(username=new_username).exists():
                errors.append('Username already taken.')
            else:
                if request.user.password is None:
                    errors.append(f'As a 42 user, your username will be changed to {new_username}_42')
                    new_username += "_42"
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'Username changed successfully.', extra_tags='change_username_tag')
                return redirect('settings')
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f'{field}: {error}')
    for error in errors:
        messages.error(request, error, extra_tags='change_username_tag')
    return redirect('settings')

@login_required
def setting_change_image(request):
    errors = []
    if request.method == 'POST':
        form = ChangeImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image changed successfully.', extra_tags='change_image_tag')
            return redirect('settings')
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f'{field}: {error}')
    for error in errors:
        messages.error(request, error, extra_tags='change_image_tag')
    return redirect('settings')

@login_required
def setting_change_password(request):
    errors = []
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            user = request.user

            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Important!
                    messages.success(request, 'Your password was successfully updated!', extra_tags='change_password_tag')
                    return redirect('settings')
                else:
                    errors.append('New passwords do not match!')
            else:
                errors.append('Incorrect old password!')
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field}: {error}")
    for error in errors:
        messages.error(request, error, extra_tags='change_password_tag')
    return redirect('settings')