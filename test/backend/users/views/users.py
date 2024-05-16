import requests, re, logging
from requests import get
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from users.models import User
from aouth.views.jwt import jwt_login_required

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

@jwt_login_required
def user_update_status(request=None, user=None, new_status=None):
    if request is not None and user is not None and new_status is not None:
        logger.debug(f"Updating status of {user.username} to {new_status}")
        if user.status == new_status:
            return
        user.status = new_status
        user.save()
    elif user is not None and new_status is not None:
        logger.debug(f"Updating status of {user.username} to {new_status}")
        if user.status == new_status:
            return
        user.status = new_status
        user.save()
    else:
        logger.error("Invalid arguments for user_update_status")

# User security
# -------------

@jwt_login_required
def user_update_twofactor(request=None, user=None, enabled=None):
    if request is not None and user is not None and enabled is not None:
        logger.debug(f"Updating twofactor {'enabled' if enabled else 'disabled'} for {user.username}")
        user.twofactor_enabled = enabled
        user.save()
    elif user is not None and enabled is not None:
        logger.debug(f"Updating twofactor {'enabled' if enabled else 'disabled'} for {user.username}")
        user.twofactor_enabled = enabled
        user.save()
    else:
        logger.error("Invalid arguments for user_update_twofactor")

def user_update_validation_code(request=None, user=None, validation_code=None, registration_validation=False):
    if request is not None and user is not None and validation_code is not None:
        logger.debug(f"Updating validation code for {user.username}")
        user.validation_code = validation_code
        user.validation_code_expiration = timezone.now() + timedelta(minutes=5)
        if user.registration_validation is False and registration_validation is True:
            user.registration_validation = registration_validation
        user.save()
    elif user is not None and validation_code is not None:
        logger.debug(f"Updating validation code for {user.username}")
        user.validation_code = validation_code
        user.validation_code_expiration = timezone.now() + timedelta(minutes=5)
        if user.registration_validation is False and registration_validation is True:
            user.registration_validation = registration_validation
        user.save()
    else:
        logger.error("Invalid arguments for user_update_validation_code")

# User game management
# --------------------

@jwt_login_required
def user_add_to_match_history(request=None, user=None, game=None):
    if request is not None and user is not None and game is not None:
        user.match_history.add(game)
        user.save()
    elif user is not None and game is not None:
        user.match_history.add(game)
        user.save()
    else:
        logger.error("Invalid arguments for user_add_to_match_history")

@jwt_login_required
def user_remove_from_match_history(request=None, user=None, game=None):
    if request is not None and user is not None and game is not None:
        user.match_history.remove(game)
        user.save()
    elif user is not None and game is not None:
        user.match_history.remove(game)
        user.save()
    else:
        logger.error("Invalid arguments for user_remove_from_match_history")

@jwt_login_required
def user_add_current_game(request=None, user=None, game=None):
    if request is not None and user is not None and game is not None:
        user.current_game = game
        user.save()
    elif user is not None and game is not None:
        user.current_game = game
        user.save()
    else:
        logger.error("Invalid arguments for user_add_current_game")

@jwt_login_required
def user_remove_current_game(request=None, user=None):
    if request is not None and user is not None:
        user.current_game = None
        user.save()
    elif user is not None:
        user.current_game = None
        user.save()
    else:
        logger.error("Invalid arguments for user_remove_current_game")
     
from matchmaking.models import MatchmakingQueue

""" @jwt_login_required
def user_get_current_game(request):
    default_queue = MatchmakingQueue.objects.get(name="remote queue")
    players = default_queue.players.all()
    contexts = 0
    if players.first():
        contexts = 1
    else:
        contexts = 2
    return JsonResponse({'context': contexts, 'current_game': request.user.current_game.id if request.user.current_game else None})
 """

@jwt_login_required
def user_get_current_game(request):
    default_queue = MatchmakingQueue.objects.get(name="remote queue")
    players = list(default_queue.players.all())
    
    # Determine the context based on the player's position in the queue or game state
    context = 0  # Default context for "no game"
    if players:
        if request.user == players[0]:
            context = 1  # User is the first player in the queue
        elif request.user in players:
            context = 2  # User is in the queue but not the first player
        else:
            context = 3  # User is neither first nor in the queue (fallback case)

    current_game_id = request.user.current_game.id if request.user.current_game else None
    return JsonResponse({'context': context, 'current_game': current_game_id})


@jwt_login_required
def user_get_last_game(request):
    if not request.user.match_history.all():
        return None
    return request.user.match_history.last()

    


# Other
# -----

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