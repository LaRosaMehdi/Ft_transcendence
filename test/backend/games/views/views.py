import logging
from django.shortcuts import render

from aouth.views.jwt import jwt_login_required, jwt_decode

logger = logging.getLogger(__name__)

# Base views
# -----------

@jwt_login_required
def view_play(request):
    return render(request, 'play.html', {'current_user': request.user})

@jwt_login_required
def view_mode(request):
    user = jwt_decode(request)
    logger.debug(f"Mode user: {user}")
    return render(request, 'mode.html')

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