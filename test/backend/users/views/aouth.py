import requests, re, logging
from requests import get
from users.models import user
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

from users.views import *

logger = logging.getLogger(__name__)

# AOUTHENTIFICATION
# -----------------

# * Login
# -------

def aouth_login(request, _user_id, _password):

    is_email = "@" in _user_id
    errors = []
    if is_email:
        user_instance = user_get_by_email(_user_id)
    else:
        user_instance = user_get_by_username(_user_id)
    if user_instance is None:
        errors.append("User not found, please register")
    elif not check_password(_password, user_instance.password):
        errors.append("Password incorrect")
    if errors:
        for error in errors:
            messages.error(request, error)
        return None
    return user_instance

def aouth_login_form(request):
    try:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            password = request.POST.get('password')
            user = aouth_login(request, user_id, password)
            if user is None:
                return HttpResponseRedirect('http://localhost:8080/api/login')
            return redirect('home', username=user.username)
        else:
            logger.error("Invalid request method")
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Exception as e:
        logger.exception("An error occurred in oauth_callback")
        return JsonResponse({'error': str(e)}, status=500)

# * Registration
# --------------

def aouth_register(request, _username, _password, _email, _image):

    def is_valid_password(password):
        if len(password) < 8:
            return False
        if not re.search(r"[a-zA-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*()-_+=]", password):
            return False
        return True
    
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email):
            return True
        return False
        
    user_by_username = user_get_by_username(_username)
    user_by_email = user_get_by_email(_email)
    errors = []
    if user_by_username is not None and user_by_username == user_by_email:
        errors.append("Already registered, please login")
    if user_by_username is not None:
        errors.append("Username already used")
    if user_by_email is not None:
        errors.append("Email already used")
    if not is_valid_password(_password):
        errors.append("Password invalid (min 8 characters, 1 letter, 1 number, 1 special character)")
    if not is_valid_email(_email):
        errors.append("Email invalid")
    if errors:
        for error in errors:
            messages.error(request, error)
        return None
    return user_create(_username, _password, _email, None)[0]
    
def aouth_register_form(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            new_user = aouth_register(request, username, password, email, None)
            if new_user is None:
                return HttpResponseRedirect('http://localhost:8080/api/register')
            return redirect('home', username=new_user.username)
        else:
            logger.error("Invalid request method")
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Exception as e:
        logger.exception("An error occurred in oauth_callback")
        return JsonResponse({'error': str(e)}, status=500)

# * 42 Oauth
# ----------

# May need to Intranet application (one to register and one to login)

def oauth_callback(request):
    logger.info(f"Authentication via 42 oauth")

    code = request.GET.get('code')
    if not code:
        logger.error("No code provided in request")
        return JsonResponse({'error': 'Code not provided'}, status=400)

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
            return JsonResponse({'error': 'Failed to fetch access token'}, status=token_response.status_code)

        access_token = token_response.json().get('access_token')
        logger.debug(f"Access token: {access_token}")

        user_response = requests.get('https://api.intra.42.fr/v2/me', headers={
            'Authorization': f'Bearer {access_token}',
        })

        if user_response.status_code != 200:
            logger.error(f"Failed to fetch user information: {user_response.json()}")
            return JsonResponse({'error': 'Failed to fetch user information'}, status=user_response.status_code)

        user_info = user_response.json()
        new_user = user_create(f"{user_info['login']}_42", None, user_info['email'], user_info['image']['link']) 
        return redirect('home', username=new_user[0].username)
    
    except Exception as e:
        logger.exception("An error occurred in oauth_callback")
        return JsonResponse({'error': str(e)}, status=500)