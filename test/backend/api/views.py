import requests, logging
from requests import get
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse

from users.models import User  
from users.views.users import *
from aouth.views.jwt import jwt_login_required
from aouth.views.forms import TwoFactorForm
from matchmaking.views.matchmaking import matchmaking

logger = logging.getLogger(__name__)

# Other views
# -----------

@jwt_login_required
def generate_profile_json(request):
    profile_instance = get_object_or_404(User, username=request.user.username)
    profile_data = {
        'username': profile_instance.username,
        'email': profile_instance.email,
        'elo': profile_instance.elo,
        'image': profile_instance.image.url
    }
    return JsonResponse(profile_data)
