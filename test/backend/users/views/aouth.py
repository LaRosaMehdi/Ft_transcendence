import requests, re, logging
from requests import get
from users.models import User
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
from users.views import *

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


# MIDDLWARE
# ---------

class AouthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in settings.MIDDLEWARE_EXEMPT_URLS):
            messages.warning(request, "You need to log in to access this page.", extra_tags="aouth_required_middleware_tag")
            return redirect('login')
        return self.get_response(request)

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
                user_set_is_connected(user)
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password", extra_tags='aouth_login_tag')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}", extra_tags='aouth_login_tag')
    user_set_is_connected(user, False)
    return redirect('login')


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
                    user_set_is_connected(user)
                    login(request, user)
                    return redirect('home')
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
    user_set_is_connected(user, True)
    return redirect('register')


# 42 OAUTH
# --------

def oauth_callback(request):
    logger.info("Authentication via 42 oauth")

    code = request.GET.get('code')
    user = None
    if not code:
        logger.error("No code provided in request")
        messages.error(request, "Code not provided")
        return redirect('register')
    
    try:
        token_response = requests.post('https://api.intra.42.fr/oauth/token', data={
            'grant_type': 'authorization_code',
            'client_id': 'u-s4t2ud-4e7c6c0a55a3674309f2425ad5c80ac4c98510374b1197a7eff37ce12371fb27',
            'client_secret': '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',
            'code': code,
            'redirect_uri': 'http://localhost:8080/api/accueil',
        })

        if token_response.status_code != 200:
            logger.error(f"Failed to fetch access token: {token_response.json()}")
            messages.error(request, "Failed to fetch access token")
            return redirect('register')

        access_token = token_response.json().get('access_token')

        user_response = requests.get('https://api.intra.42.fr/v2/me', headers={
            'Authorization': f'Bearer {access_token}',
        })

        if user_response.status_code != 200:
            logger.error(f"Failed to fetch user information: {user_response.json()}")
            messages.error(request, "Failed to fetch user information")
            return redirect('register')

        user_info = user_response.json()
        User = get_user_model()
        user_email = user_info['email']
        user = User.objects.filter(email=user_email).first()
        if not user:
            user = User.objects.create_user(username=f"{user_info['login']}_42", email=user_email, image_url=user_info['image']['link'])
        user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
        user_set_is_connected(user)
        login(request, user)
        return redirect('home')

    except Exception as e:
        logger.exception("An error occurred in oauth_callback")
        messages.error(request, "An error occurred")
        if user is not None:
            user_set_is_connected(user, False)
        return redirect('register')

# Lougout
# -------
    
def aouth_logout(request):
    if request.user.is_authenticated:
        user_set_is_connected(request.user, False)
        logout(request)
    return redirect('login')
    