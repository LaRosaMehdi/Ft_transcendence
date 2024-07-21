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
from django.template.loader import render_to_string

from users.models import User
from aouth.views.forms import *
from aouth.views.jwt import jwt_login_required, jwt_login_required, jwt_decode
from users.views.users import user_update_status, user_update_validation, user_get_from_session
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
    logger.info("Sending two-factor authentication code")
    user = jwt_decode(request)
    user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
    validation_code, hashed_validation_code = generate_validation_code()
    user.validation_code = hashed_validation_code
    if user.is_verified is False:
        user.validation_code_expiration = timezone.now() + timedelta(minutes=1)
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
    errors = []
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            validation_code = form.cleaned_data['validation_code']
            user = jwt_decode(request)
            if user:
                hashed_validation_code_entered = hashlib.sha256(validation_code.encode()).hexdigest()
                if user.validation_code == hashed_validation_code_entered:
                    user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
                    login(request, user)
                    user_update_validation(request, user, None, None, True)
                    user_update_status(request, user, 'online')
                    response_data = {
                        'status': 'success',
                        'message': 'Login Success, welcome',
                        'redirectUrl': 'home',
                        'access_token': request.session.get('access_token'),
                        'refresh_token': request.session.get('refresh_token'),
                        'csrf_token': request.META.get('CSRF_COOKIE'),
                    }
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse(response_data)
                    else:
                        response = redirect('home')
                        response.set_cookie('access_token', request.session.get('access_token'))
                        response.set_cookie('refresh_token', request.session.get('refresh_token'))
                        response.set_cookie('csrf_token', request.META.get('CSRF_COOKIE'))
                        return response
                else:
                    user_update_status(request, user, 'offline')
                    errors.append("Invalid validation code")
            else:
                errors.append("User not found")
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{error}")
    else:
        errors.append("Invalid request method")

    error_messages = ', '.join(errors)
    return JsonResponse({
        'status': 'error',
        'message': error_messages,
        'redirectUrl': 'twofactor',
    })

# Middleware
# ----------

def twofactor_auto_delete(request, bruteforce='false'):
    bruteforce = bruteforce.lower() == 'true'
    user = user_get_from_session(request)
    if user and user.is_verified is not True:
        if user.validation_code_expiration < timezone.now() or bruteforce:
            logger.info(f"Deleting unverified user {user.username}")
            user.delete()
            messages.error(request, "Validation code expired, registration canceled", extra_tags='aouth_register_tag')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                html = render_to_string('spa_register.html', {'form': RegistrationForm()}, request=request)
                return JsonResponse({'html': html})
            else:
                return render(request, 'register.html', {'form': RegistrationForm()})
    return JsonResponse({'status': 'error', 'message': 'User not found', 'redirectUrl': 'home'})