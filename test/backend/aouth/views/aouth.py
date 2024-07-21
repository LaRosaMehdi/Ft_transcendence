import requests, re, logging
from datetime import datetime, timedelta
from django.utils.timezone import now
from requests import get
from django.urls import reverse
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from aouth.views.forms import *
from aouth.views.jwt import *
from users.models import User
from aouth.views.jwt import jwt_create
from users.views.users import user_update_status
from aouth.views.twofactor import twofactor_oauth_send

logger = logging.getLogger(__name__)

# AOUTHENTIFICATION
# -----------------

class AouthUser(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user_obj = User.objects.get(username=username)
            if user_obj.check_password(password):
                return user_obj
        except User.DoesNotExist:
            return None

# LOGIN
# -----

def aouth_login_form(request):
    errors = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            if '@' in user_id:
                user = authenticate(request, email=user_id, password=password)
            else:
                user = authenticate(request, username=user_id, password=password)
            if user is not None:
                jwt_create(request, user)
                if user.twofactor_enabled:
                    return twofactor_oauth_send(request)
                return aouth_login(request, user)
            else:
                errors.append("Invalid username or password")
        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field}: {error}")

    error_messages = ', '.join(errors)
    return JsonResponse({
        'status': 'error',
        'message': error_messages,
        'redirectUrl': 'login',
    })


# REGISTRATION
# ------------


def aouth_register_form(request):
    errors = []
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    jwt_create(request, user)
                    return twofactor_oauth_send(request)
                else:
                    errors.append("Failed to authenticate user after registration")
            
            except IntegrityError as e:
                if 'username' in e.args[0]:
                    errors.append("Username already exists")
                if 'email' in e.args[0]:
                    errors.append("Email already exists")

        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field}: {error}")

    error_messages = ', '.join(errors)
    return JsonResponse({
        'status': 'error',
        'message': error_messages,
        'redirectUrl': 'register',
    })

# 42 OAUTH REGISTRATION
# ---------------------

def aouth_callback_register(request):
    logger.info("Authentication via 42 oauth")

    code = request.GET.get('code')
    if not code:
        logger.error("No code provided in request")
        messages.error(request, "Code not provided", extra_tags='aouth_callback_register')
        return redirect('register')

    try:
        token_response = requests.post('https://api.intra.42.fr/oauth/token', data={
            'grant_type': 'authorization_code',
            'client_id': settings.OAUTH_REGISTER_CLIENT_ID,
            'client_secret': settings.OAUTH_REGISTER_CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.OAUTH_REGISTER_REDIRECT_URI,
        })

        if token_response.status_code != 200:
            logger.error(f"Failed to fetch access token: {token_response.json()}")
            messages.error(request, "Failed to fetch access token", extra_tags='aouth_callback_register')
            return redirect('register')

        access_token = token_response.json().get('access_token')

        user_response = requests.get('https://api.intra.42.fr/v2/me', headers={
            'Authorization': f'Bearer {access_token}',
        })

        if user_response.status_code != 200:
            logger.error(f"Failed to fetch user information: {user_response.json()}")
            messages.error(request, "Failed to fetch user information", extra_tags='aouth_callback_register')
            return redirect('register')

        user_info = user_response.json()
        User = get_user_model()
        user_email = user_info['email']
        user = User.objects.filter(email=user_email).first()
        if user:
            messages.error(request, "You are already registered.", extra_tags='aouth_callback_register')
            return redirect('register')

        user = User.objects.create_user(username=f"{user_info['login']}_42", email=user_email, image_url=user_info['image']['link'])
        jwt_create(request, user)
        return twofactor_oauth_send(request)

    except Exception as e:
        logger.exception("An error occurred in oauth_callback_register")
        messages.error(request, "An error occurred during registration", extra_tags='aouth_callback_register')
        return redirect('register')

# 42 OAUTH LOGIN
# --------------

def aouth_callback_login(request):
    logger.info("Authentication via 42 oauth")

    code = request.GET.get('code')
    if not code:
        logger.error("No code provided in request")
        messages.error(request, "Code not provided", extra_tags='aouth_callback_login')
        return redirect('login')

    try:
        token_response = requests.post('https://api.intra.42.fr/oauth/token', data={
            'grant_type': 'authorization_code',
            'client_id': settings.AOUTH_LOGIN_CLIENT_ID,
            'client_secret': settings.OAUTH_LOGIN_CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.AOUTH_LOGIN_REDIRECT_URI,
        })

        if token_response.status_code != 200:
            logger.error(f"Failed to fetch access token: {token_response.json()}")
            messages.error(request, "Failed to fetch access token", extra_tags='aouth_callback_login')
            return redirect('login')

        access_token = token_response.json().get('access_token')

        user_response = requests.get('https://api.intra.42.fr/v2/me', headers={
            'Authorization': f'Bearer {access_token}',
        })

        if user_response.status_code != 200:
            logger.error(f"Failed to fetch user information: {user_response.json()}")
            messages.error(request, "Failed to fetch user information", extra_tags='aouth_callback_login')
            return redirect('login')

        user_info = user_response.json()
        User = get_user_model()
        user_email = user_info['email']
        user = User.objects.filter(email=user_email).first()
        if not user:
            messages.error(request, "You are not registered. Please register first.", extra_tags='aouth_callback_login')
            return redirect('login')
        jwt_create(request, user)
        if user.twofactor_enabled is True:
            return twofactor_oauth_send(request)
        return aouth_login(request, user)
    
    except Exception as e:
        logger.exception("An error occurred in aouth_callback_login")
        messages.error(request, "An error occurred during login", extra_tags='aouth_callback_login')
        return redirect('login')

# LOGIN
# -----

def aouth_login(request, user):
    user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'     
    login(request, user)
    user_update_status(request, user, 'online')
    response_data = {
        'status': 'success',
        'message': 'Login Success, welcome',
        'redirectUrl': 'home',
        'access_token': request.session.get('access_token'),
        'refresh_token': request.session.get('refresh_token'),
        'csrf_token': request.META.get('CSRF_COOKIE')
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(response_data)
    return render(request, 'loading_connection.html', {
        'access_token': response_data['access_token'],
        'refresh_token': response_data['refresh_token'],
        'csrf_token': response_data['csrf_token'],
        'redirect_url': 'home',
    })


# LOUGOUT
# -------

# class AouthTimeoutLogoutAutoMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             current_time = now()
#             last_activity = request.session.get('last_activity')

#             if last_activity:
#                 last_activity_time = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')
#                 if current_time - last_activity_time > timedelta(seconds=30):
#                     aouth_logout(request)
#                     return self.logout_response(request)

#             request.session['last_activity'] = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')

#         response = self.get_response(request)
#         return response




class AouthLogoutAutoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            if request.path == '/aouth/register/':
                return aouth_logout(request, redirect_url='register')
            if request.path == '/aouth/login/' or request.path == '/aouth/twofactor/':
                return aouth_logout(request)
        return response

@csrf_exempt
@jwt_login_required
def aouth_logout(request, redirect_url='login'):
    response = redirect(redirect_url)
    if request.user.is_authenticated:
        user_update_status(request, request.user, 'offline')
        jwt_destroy(request, response)
        logout(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('spa_login.html', request=request)
        return JsonResponse({'html': html})
    else: 
        return response

@jwt_login_required
def aouth_logout_popstate(request, redirect_url='login'):
    logger.info("YUU")
    response = redirect(redirect_url)
    if request.user.is_authenticated:
        user_update_status(request, request.user, 'offline')
        jwt_destroy(request, response)
        logout(request)
    
    return JsonResponse({'message': 'loggout'})