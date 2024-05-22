import logging
from django.shortcuts import render

from users.views.users import user_get_last_game
from aouth.views.jwt import jwt_login_required, jwt_decode

logger = logging.getLogger(__name__)

# Base views
# -----------

@jwt_login_required
def view_play(request, game_id=None):
    return render(request, 'play.html', {'game_id': game_id, 'game': user_get_last_game(request)})

@jwt_login_required
def view_mode(request):
    user = jwt_decode(request)
    logger.debug(f"Mode user: {user}")
    return render(request, 'mode.html')

@jwt_login_required
def view_results(request):
    return render(request, 'results.html', {'game': user_get_last_game(request)})

# Modes
# -----

@jwt_login_required
def view_remote(request):
    user = jwt_decode(request)
    logger.debug(f"Remote user: {user}")
    return render(request, 'remote.html')

@jwt_login_required
def view_vscomputer(request):
    user = jwt_decode(request)
    logger.debug(f"Remote user: {user}")
    return render(request, 'vscomputer.html')

# Others ??
# ---------

@jwt_login_required
def view_main_chat(request):
    user = jwt_decode(request)
    logger.debug(f"Remote user: {user}")
    return render(request, 'main_chat.html')

@jwt_login_required
def view_game_in_progress(request):
    return render(request, 'game_progress.html')