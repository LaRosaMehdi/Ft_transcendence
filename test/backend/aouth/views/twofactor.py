import logging, hashlib, random
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from aouth.views.jwt import jwt_login_required, jwt_login_required, jwt_decode
from users.views.users import user_update_status
from aouth.views.forms import TwoFactorForm
from smtp.views import smtp_aouth_validation
from aouth.views.jwt import jwt_login_required

logger = logging.getLogger(__name__)

# Generate a 6-digit validation code
# ----------------------------------

def generate_validation_code():
    validation_code = ''.join(random.choices('0123456789', k=6))
    hashed_validation_code = hashlib.sha256(validation_code.encode()).hexdigest()
    return validation_code, hashed_validation_code

# TWO FACTOR AOUTH (42, register & login)
# ---------------------------------------

def twofactor_oauth_send(request):
    user = jwt_decode(request)
    user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
    validation_code, hashed_validation_code = generate_validation_code()
    user.validation_code = hashed_validation_code
    user.save()
    smtp_aouth_validation(user, validation_code)
    request.session['user_id'] = user.id
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Two-factor authentication code sent. Please check your email.',
            'redirectUrl': 'twofactor',
        })
    else:
        return redirect('twofactor')

def twofactor_oauth(request):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            validation_code = form.cleaned_data['validation_code']
            user = jwt_decode(request)
            if user:
                hashed_validation_code_entered = hashlib.sha256(validation_code.encode()).hexdigest()
                if user.validation_code == hashed_validation_code_entered:
                    user.validation_code = None
                    user.save()
                    user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'     
                    login(request, user)
                    user_update_status(request, user, 'online')
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Login Sucess, welcome',
                            'redirectUrl': 'home',
                        })
                    else:
                        return redirect('home')
            
                else:
                    user_update_status(user, 'offline')
                    messages.error(request, "Invalid validation code", extra_tags='twofactor_oauth_tag')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}", extra_tags='twofactor_oauth_tag')
    else:
        messages.error(request, "Invalid request method", extra_tags='twofactor_oauth_tag')
    return JsonResponse({
        'status': 'error',
        'message': 'error',
        'redirectUrl': 'home',
    })