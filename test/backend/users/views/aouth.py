import requests, re, logging
from requests import get
from users.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
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
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password", extra_tags='aouth_login_tag')
    return render(request, 'login.html', {'form': LoginForm()})

# REGISTRATION
# ------------

def aouth_register_form(request):
    errors = []
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User {username} registered and authenticated")
                return redirect('home')
            else:
                errors.append("Failed to authenticate user after registration")
                logger.error("Failed to authenticate user after registration")
        else:
            errors.append("Invalid registration form")
            logger.error("Invalid registration form")
    if errors != []:
        for error in errors:
            messages.error(request, error, extra_tags='aouth_register_tag')
    return render(request, 'register.html', {'form': form})


# 42 OAUTH
# --------

from django.contrib.auth import get_user_model

def oauth_callback(request):
    logger.info("Authentication via 42 oauth")

    code = request.GET.get('code')
    if not code:
        logger.error("No code provided in request")
        messages.error(request, "Code not provided")
        return render(request, 'register.html')

    logger.debug(f"Code received: {code}")

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
            return render(request, 'register.html')

        access_token = token_response.json().get('access_token')
        logger.debug(f"Access token: {access_token}")

        user_response = requests.get('https://api.intra.42.fr/v2/me', headers={
            'Authorization': f'Bearer {access_token}',
        })

        if user_response.status_code != 200:
            logger.error(f"Failed to fetch user information: {user_response.json()}")
            messages.error(request, "Failed to fetch user information")
            return render(request, 'register.html')

        user_info = user_response.json()

        User = get_user_model()
        user = User.objects.filter(username=f"{user_info['login']}_42").first()
        logger.debug(f"User: {user_info['image']['link']}")
        if not user:
            user = User.objects.create_user(username=f"{user_info['login']}_42", email=user_info['email'], image_url=user_info['image']['link'])
        user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
        login(request, user)
        return redirect('home')

    except Exception as e:
        logger.exception("An error occurred in oauth_callback")
        messages.error(request, "An error occurred")
        return render(request, 'register.html', {'form': RegistrationForm()})