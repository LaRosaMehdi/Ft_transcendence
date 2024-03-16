import requests, re, logging
from requests import get
from users.models import User
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

# USER MANAGEMENT
# ---------------

def user_get_by_username(_login):
    return User.objects.filter(username=_login).first()

def user_get_by_email(_email):
    return User.objects.filter(email=_email).first()

def user_create(_login, _password, _email, _img):
    existing_user = user_get_by_username(_login)
    if existing_user:
        logger.info(f"User already exists: {existing_user}")
        return existing_user, True
    hashed_password = make_password(_password) if _password else None
    new_user = User.objects.create(
        username=_login,
        email=_email,
        password=hashed_password,  # Use hashed password
        image=_img
    )
    logger.info(f"New user created: {new_user}")
    return new_user, False