from django.shortcuts import render
from django.http import HttpResponseRedirect
from users.models import user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
import requests
from requests import get
import logging

logger = logging.getLogger(__name__)

def create_users(_login, _password, _email, _img):
    existing_user = user.objects.filter(username=_login).first()
    if existing_user:
        return existing_user, False
    hashed_password = make_password(_password) if _password else None
    new_user = user.objects.create(
        username=_login,
        email=_email,
        password=hashed_password,  # Use hashed password
        image=_img
    )
    logger.info(f"New user created: {new_user}")
    return new_user, True

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
        logger.debug(f"User info: {user_info['login']}")
        create_users(user_info['login'], None, user_info['email'], user_info['image']['link'])
        
        return redirect('http://localhost:8080/users/accueil2/')
    except Exception as e:
        logger.exception("An error occurred in oauth_callback")
        return JsonResponse({'error': str(e)}, status=500)
    
def oauth_form(request):
    try:
        logger.info(f"Authentication via form")
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            create_users(username, password, email, None)
            return redirect('http://localhost:8080/users/accueil2/')
        else:
            logger.error("Invalid request method")
            return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Exception as e:
        logger.exception("An error occurred in oauth_callback")
        return JsonResponse({'error': str(e)}, status=500)