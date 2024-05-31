import requests, re, logging
from requests import get
from django.urls import reverse
from django.conf import settings
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.template.loader import render_to_string

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
                if user.twofactor_enabled is True:
                    return twofactor_oauth_send(request)
                return aouth_login(request, user)
            else:
                messages.error(request, "Invalid username or password", extra_tags='aouth_login_tag')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}", extra_tags='aouth_login_tag')
    return JsonResponse({
        'status': 'error',
        'message': 'error.',
        'redirectUrl': 'login',
    })


# REGISTRATION
# ------------

def aouth_register_form(request):
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
                    messages.error(request, "Failed to authenticate user after registration", extra_tags='aouth_register_tag')
            
            except IntegrityError as e:
                if 'username' in e.args[0]:  # Check if the error is related to the username field
                    messages.error(request, "Username already exists", extra_tags='aouth_register_tag')
                if 'email' in e.args[0]:  # Check if the error is related to the email field
                    messages.error(request, "Email already exists", extra_tags='aouth_register_tag')

        else:
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    messages.error(request, f"{field}: {error}", extra_tags='aouth_register_tag')
    return JsonResponse({
        'status': 'error',
        'message': 'error.',
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
    
    response = redirect('home')
    response.set_cookie('access_token', request.session.get('access_token'))
    response.set_cookie('refresh_token', request.session.get('refresh_token'))
    response.set_cookie('csrf_token', request.META.get('CSRF_COOKIE'))
    return response
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     return JsonResponse({
    #         'status': 'success',
    #         'message': 'Login Sucess, welcome',
    #         'redirectUrl': 'home',
    #     })
    # return redirect('home')

# LOUGOUT
# -------

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
    