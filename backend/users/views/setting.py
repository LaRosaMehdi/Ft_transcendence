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
    warning = None
    
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
                    warning = f'As a 42 user, your username will be changed to {new_username}_42'
                    new_username += "_42"
                    
                request.user.username = new_username
                request.user.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'warning': warning if warning else '',
                        'message': 'Username changed successfully.',
                        'redirectUrl': 'settings',
                    })
                else:
                    return redirect('settings')
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    errors.append(f'{error}')
    
    if errors:
        error_messages = ', '.join(errors)
        logger.debug(f"Errors: {error_messages}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': error_messages,
                'redirectUrl': 'settings',
            })
        
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
                    'message': 'Image changed successfully.',
                    'image': request.user.image.url,
                    'redirectUrl': 'settings',
                })
            else:
                return redirect('settings')
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f'{field}: {error}')
    if errors:
        error_messages = ', '.join(errors)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': error_messages,
                'image': request.user.image.url,
                'redirectUrl': 'settings',
            })
    else:
        return redirect('settings')

@login_required
def setting_change_password(request):
    errors = []
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        logger.debug(f"ChangePasswordForm validity: {form.is_valid()}")
        
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            user = request.user
            
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)  # Use set_password to hash the new password
                    user.save()
                    update_session_auth_hash(request, user)  # Update session to prevent logout
                    logger.debug("Password was successfully updated.")
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Your password was successfully updated!',
                            'redirectUrl': 'settings',  # Redirect URL for client-side handling
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
    
    # Handle AJAX request errors
    if errors:
        error_messages = ', '.join(errors)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': error_messages,
                'redirectUrl': 'settings',  # Include redirect URL if needed
            })
    
    # Handle non-AJAX request redirection
    return redirect('settings')


@jwt_login_required
def setting_change_2fa(request):
    errors = []
    if request.method == 'POST':
        form = Change2faForm(request.POST)
        if form.is_valid():
            enable_2fa = form.cleaned_data['enable_2fa']
            user_update_twofactor(request=request, user=request.user, enabled=enable_2fa)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': f"2FA {'enabled' if enable_2fa is True else 'disabled'} successfully.",
                    'redirectUrl': 'settings',
                })
            else:
                return redirect('settings')
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f'{field}: {error}')
    if errors:
        error_messages = ', '.join(errors)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': error_messages,
                'redirectUrl': 'settings',
            })
    else:
        return redirect('settings')