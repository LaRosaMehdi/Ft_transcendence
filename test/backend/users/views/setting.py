import requests, re, logging
from requests import get
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

from users.models import User
from users.views.forms import *
from users.views.users import user_update_twofactor
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

# SETTINGS
# --------

@jwt_login_required
def setting_change_username(request):
    errors = []
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            if request.user.username == new_username or request.user.username == f'{new_username}_42':
                errors.append('New username is the same as the current one.')
            elif User.objects.filter(username=new_username).exists():
                errors.append('Username already taken.')
            else:
                if request.user.password is None:
                    messages.warning(request, f'As a 42 user, your username will be changed to {new_username}_42', extra_tags='change_username_tag')
                    new_username += "_42"
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'Username changed successfully.', extra_tags='change_username_tag')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Setting change User-Name',
                        'redirectUrl': 'settings',
                    })
                else:
                    return redirect('settings')
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f'{field}: {error}')
    for error in errors:
        messages.error(request, error, extra_tags='change_username_tag')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Setting change User-Name',
            'redirectUrl': 'settings',
        })
    else:
        return redirect('settings')

@jwt_login_required
def setting_change_image(request):
    errors = []
    if request.method == 'POST':
        form = ChangeImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image changed successfully.', extra_tags='change_image_tag')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Setting change Image',
                    'redirectUrl': 'settings',
                })
            else:
                return redirect('settings')
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f'{field}: {error}')
    for error in errors:
        messages.error(request, error, extra_tags='change_image_tag')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Setting change Image',
            'redirectUrl': 'settings',
        })
    else:
        return redirect('settings')

@login_required
def setting_change_password(request):
    errors = []
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        logger.debug(f"twofactor_setting: { form.is_valid()}")
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            user = request.user
            if user.check_password(old_password):
                if new_password == confirm_password:
                    hashed_new_password = make_password(new_password)  # Hash the new password
                    if hashed_new_password:
                        user.password = hashed_new_password
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Your password was successfully updated!', extra_tags='change_password_tag')
                        logger.debug(f"twofactor_setting: Your password was successfully updated!")
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'status': 'success',
                                'message': 'Setting change Password',
                                'redirectUrl': 'settings',
                            })
                        else:
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
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Setting change Password',
            'redirectUrl': 'settings',
        })
    else:
        return redirect('settings')

@jwt_login_required
def setting_change_2fa(request):
    errors = []
    if request.method == 'POST':
        form = Change2faForm(request.POST)
        if form.is_valid():
            enable_2fa = form.cleaned_data['enable_2fa']
            user_update_twofactor(request=request, user=request.user, enabled=enable_2fa)
            messages.success(request, f'2FA {"enabled" if enable_2fa is True else "disabled"} successfully.', extra_tags='change_2fa_tag')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Setting change 2FA',
                    'redirectUrl': 'settings',
                })
            else:
                return redirect('settings')
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f'{field}: {error}')
    for error in errors:
        messages.error(request, error, extra_tags='change_2fa_tag')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Setting change 2FA',
            'redirectUrl': 'settings',
        })
    else:
        return redirect('settings')